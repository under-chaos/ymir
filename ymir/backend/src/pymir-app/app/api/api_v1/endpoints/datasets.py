import pathlib
import random
import tempfile
from dataclasses import dataclass
from typing import Any, Optional, Dict, List
from zipfile import BadZipFile

from fastapi import APIRouter, BackgroundTasks, Depends, Path, Query
from fastapi.logger import logger
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.api.errors.errors import (
    AssetNotFound,
    DatasetNotFound,
    DuplicateDatasetError,
    FailedtoCreateDataset,
    FailedtoDownloadError,
    FieldValidationFailed,
    NoDatasetPermission,
)
from app.config import settings
from app.models.task import TaskState, TaskType
from app.utils.files import (
    FailedToDownload,
    is_valid_import_path,
    prepare_dataset,
)
from app.utils.stats import RedisStats
from app.utils.ymir_controller import ControllerClient, ControllerRequest
from app.utils.ymir_viz import VizClient
from app.utils.class_ids import get_keyword_id_to_name_mapping

router = APIRouter()


@router.get(
    "/", response_model=schemas.DatasetOut,
)
def list_dataset(
    db: Session = Depends(deps.get_db),
    dataset_ids: str = Query(None, example="12,13,14", alias="ids"),
    name: str = Query(None, description="search by dataset's name"),
    type_: models.task.TaskType = Query(
        None, alias="type", description="type of related task"
    ),
    state: models.task.TaskState = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
    start_time: int = Query(None, description="from this timestamp"),
    end_time: int = Query(None, description="to this timestamp"),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get list of datasets,
    pagination is supported by means of offset and limit
    """
    if dataset_ids:
        ids = [int(i) for i in dataset_ids.split(",")]
        datasets = crud.dataset.get_multi_by_ids(db, ids=ids)
        if not datasets:
            raise DatasetNotFound()
        total = len(datasets)
    else:
        datasets, total = crud.dataset.get_multi_datasets(
            db,
            user_id=current_user.id,
            name=name,
            type_=type_,
            state=state,
            offset=offset,
            limit=limit,
            start_time=start_time,
            end_time=end_time,
        )
    return {"result": {"total": total, "items": datasets}}


@router.get(
    "/public", response_model=schemas.DatasetOut,
)
def get_public_datasets(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all the public datasets,
    public datasets come from User 1
    """
    datasets, total = crud.dataset.get_datasets_of_user(
        db, user_id=settings.PUBLIC_DATASET_OWNER,
    )
    return {"result": {"total": total, "items": datasets}}


@router.post(
    "/", response_model=schemas.DatasetOut,
)
def create_dataset(
    *,
    db: Session = Depends(deps.get_db),
    dataset_import: schemas.DatasetImport,
    current_user: models.User = Depends(deps.get_current_active_user),
    current_workspace: models.Workspace = Depends(deps.get_current_workspace),
    controller_client: ControllerClient = Depends(deps.get_controller_client),
    background_tasks: BackgroundTasks,
) -> Any:
    """
    Create dataset.

    Three Import Strategy:
    - no_annotations = 1
    - ignore_unknown_annotations = 2
    - stop_upon_unknown_annotations = 3
    """
    dataset = crud.dataset.get_by_user_and_name(
        db, user_id=current_user.id, name=dataset_import.name
    )
    if dataset:
        raise DuplicateDatasetError()

    pre_dataset = PrepareDataset.from_dataset_input(
        current_user.id, current_workspace.hash, dataset_import
    )

    task_in = schemas.TaskCreate(name=pre_dataset.task_id, type=pre_dataset.task_type)
    task = crud.task.create_task(
        db, obj_in=task_in, task_hash=pre_dataset.task_id, user_id=current_user.id
    )
    # todo: better way to hide task of importing data
    crud.task.soft_remove(db, id=task.id)
    logger.info("[create dataset] task created and hided: %s", task)

    dataset_in = schemas.DatasetCreate(
        name=dataset_import.name,
        hash=pre_dataset.task_id,
        type=pre_dataset.task_type,
        user_id=current_user.id,
        task_id=task.id,
    )
    dataset = crud.dataset.create(db, obj_in=dataset_in)
    logger.info("[create dataset] dataset record created: %s", dataset)

    # run background task when related task record has been created
    background_tasks.add_task(
        import_dataset, db, controller_client, pre_dataset, task.id
    )

    return {"result": dataset}


@dataclass
class PrepareDataset:
    user_id: int
    workspace: Optional[str]
    src_url: Optional[str]
    src_dataset_id: Optional[int]
    src_path: Optional[str]
    task_type: TaskType
    task_id: str
    strategy: schemas.ImportStrategy

    @classmethod
    def from_dataset_input(
        cls,
        user_id: int,
        workspace: Optional[str],
        dataset_import: schemas.DatasetImport,
    ) -> "PrepareDataset":
        if dataset_import.input_url or dataset_import.input_path:
            task_type = TaskType.import_data
        elif dataset_import.input_dataset_id:
            task_type = TaskType.copy_data
        else:
            logger.exception(
                "[create dataset] refuse to create dataset without url or dataset_id"
            )
            raise FailedtoCreateDataset()
        task_id = ControllerRequest.gen_task_id(user_id)
        return cls(
            user_id=user_id,
            workspace=workspace,
            src_url=dataset_import.input_url,
            src_dataset_id=dataset_import.input_dataset_id,
            src_path=dataset_import.input_path,
            task_type=task_type,
            task_id=task_id,
            strategy=dataset_import.strategy,
        )


def import_dataset(
    db: Session,
    controller_client: ControllerClient,
    pre_dataset: PrepareDataset,
    task_id: int,
) -> None:
    try:
        _import_dataset(db, controller_client, pre_dataset)
    except (BadZipFile, FailedToDownload, FailedtoCreateDataset, DatasetNotFound) as e:
        logger.error("[create dataset] failed to import dataset: %s", e)
        crud.task.update_task_state(db, task_id=task_id, new_state=TaskState.error)


def _import_dataset(
    db: Session, controller_client: ControllerClient, pre_dataset: PrepareDataset
) -> None:
    parameters = {}  # type: Dict[str, Any]
    if pre_dataset.src_url is not None:
        # Controller will read this directory later
        # so temp_dir will not be removed here
        temp_dir = tempfile.mkdtemp(
            prefix="import_dataset_", dir=settings.SHARED_DATA_DIR
        )
        paths = prepare_dataset(pre_dataset.src_url, temp_dir)
        if "annotations" not in paths or "images" not in paths:
            raise FailedtoCreateDataset()
        parameters = {
            "annotation_dir": str(paths["annotations"]),
            "asset_dir": str(paths["images"]),
        }
    elif pre_dataset.src_path is not None:
        src_path = pathlib.Path(pre_dataset.src_path)
        if not is_valid_import_path(src_path):
            raise FailedtoCreateDataset()
        parameters = {
            "annotation_dir": str(src_path / "annotations"),
            "asset_dir": str(src_path / "images"),
        }
    elif pre_dataset.src_dataset_id is not None:
        dataset = crud.dataset.get(db, id=pre_dataset.src_dataset_id)
        if not dataset:
            raise DatasetNotFound()
        user_id = f"{dataset.user_id:0>4}"
        repo_id = f"{dataset.user_id:0>6}"
        parameters = {
            "src_user_id": user_id,
            "src_repo_id": repo_id,
            "src_dataset_id": dataset.hash,
        }

    parameters["strategy"] = pre_dataset.strategy
    req = ControllerRequest(
        pre_dataset.task_type,
        pre_dataset.user_id,
        pre_dataset.workspace,
        pre_dataset.task_id,
        args=parameters,
    )
    logger.info("[create dataset] controller request: %s", req)

    try:
        resp = controller_client.send(req)
        logger.info("[create dataset] controller response: %s", resp)
    except ValueError as e:
        # todo parse error message
        logger.exception("[create dataset] controller error: %s", e)
        raise FailedtoCreateDataset()


@router.delete(
    "/{dataset_id}",
    response_model=schemas.DatasetOut,
    dependencies=[Depends(deps.get_current_active_user)],
    responses={
        400: {"description": "No permission"},
        404: {"description": "Dataset Not Found"},
    },
)
def delete_dataset(
    *,
    db: Session = Depends(deps.get_db),
    dataset_id: int = Path(..., example="12"),
    current_user: models.User = Depends(deps.get_current_active_user),
    stats_client: RedisStats = Depends(deps.get_stats_client),
) -> Any:
    """
    Delete dataset
    (soft delete actually)
    """
    dataset = crud.dataset.get(db, id=dataset_id)
    if not dataset:
        raise DatasetNotFound()
    if dataset.user_id != current_user.id:
        raise NoDatasetPermission()
    dataset = crud.dataset.soft_remove(db, id=dataset_id)
    stats_client.delete_dataset_rank(current_user.id, dataset_id)
    return {"result": dataset}


@router.get(
    "/{dataset_id}",
    response_model=schemas.DatasetOut,
    dependencies=[Depends(deps.get_current_active_user)],
    responses={404: {"description": "Dataset Not Found"}},
)
def get_dataset(
    db: Session = Depends(deps.get_db),
    dataset_id: int = Path(..., example="12"),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get verbose information of specific dataset
    """
    dataset = crud.dataset.get_with_task(db, user_id=current_user.id, id=dataset_id)
    if not dataset:
        raise DatasetNotFound()
    return {"result": dataset}


@router.patch(
    "/{dataset_id}",
    response_model=schemas.DatasetOut,
    responses={404: {"description": "Dataset Not Found"}},
)
def update_dataset_name(
    *,
    db: Session = Depends(deps.get_db),
    dataset_id: int = Path(..., example="12"),
    dataset_in: schemas.DatasetUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update dataset name
    """
    if not dataset_in.name:
        raise FieldValidationFailed()

    dataset = crud.dataset.get_by_user_and_name(
        db, user_id=current_user.id, name=dataset_in.name
    )
    if dataset:
        raise DuplicateDatasetError()

    dataset = crud.dataset.get(db, id=dataset_id)
    if not dataset:
        raise DatasetNotFound()
    dataset = crud.dataset.update(db, db_obj=dataset, obj_in=dataset_in)
    return {"result": dataset}


@router.get(
    "/{dataset_id}/assets",
    response_model=schemas.AssetOut,
    responses={404: {"description": "Dataset Not Found"}},
)
def get_assets_of_dataset(
    db: Session = Depends(deps.get_db),
    dataset_id: int = Path(..., example="12"),
    offset: int = 0,
    limit: int = settings.DEFAULT_LIMIT,
    keyword: Optional[str] = Query(None),
    keyword_id: Optional[int] = Query(None),
    viz_client: VizClient = Depends(deps.get_viz_client),
    current_user: models.User = Depends(deps.get_current_active_user),
    current_workspace: models.Workspace = Depends(deps.get_current_workspace),
    labels: List[str] = Depends(deps.get_personal_labels),
) -> Any:
    """
    Get asset list of specific dataset,
    pagination is supported by means of offset and limit
    """
    dataset = crud.dataset.get_with_task(db, user_id=current_user.id, id=dataset_id)
    if not dataset:
        raise DatasetNotFound()

    keyword_id_to_name = get_keyword_id_to_name_mapping(labels)
    keyword_name_to_id = {v: k for k, v in keyword_id_to_name.items()}
    logger.info(
        "keyword_id_to_name: %s, keyword_name_to_id: %s",
        keyword_id_to_name,
        keyword_name_to_id,
    )

    keyword_id = keyword_id or keyword_name_to_id.get(keyword)

    viz_client.config(
        user_id=current_user.id,
        repo_id=current_workspace.hash,
        branch_id=dataset.task_hash,  # type: ignore
        keyword_id_to_name=keyword_id_to_name,
    )
    assets = viz_client.get_assets(keyword_id=keyword_id, limit=limit, offset=offset)
    result = {
        "keywords": assets.keywords,
        "items": assets.items,
        "total": assets.total,
    }
    return {"result": result}


@router.get(
    "/{dataset_id}/assets/random",
    response_model=schemas.AssetOut,
    responses={404: {"description": "Asset Not Found"}},
)
def get_random_asset_id_of_dataset(
    db: Session = Depends(deps.get_db),
    dataset_id: int = Path(..., example="12"),
    viz_client: VizClient = Depends(deps.get_viz_client),
    current_user: models.User = Depends(deps.get_current_active_user),
    current_workspace: models.Workspace = Depends(deps.get_current_workspace),
    labels: List[str] = Depends(deps.get_personal_labels),
) -> Any:
    """
    Get random asset from specific dataset
    """
    dataset = crud.dataset.get_with_task(db, user_id=current_user.id, id=dataset_id)
    if not dataset:
        raise DatasetNotFound()

    keyword_id_to_name = get_keyword_id_to_name_mapping(labels)
    offset = get_random_asset_offset(dataset)
    viz_client.config(
        user_id=current_user.id,
        repo_id=current_workspace.hash,
        branch_id=dataset.task_hash,  # type: ignore
        keyword_id_to_name=keyword_id_to_name,
    )
    assets = viz_client.get_assets(keyword_id=None, offset=offset, limit=1,)
    if assets.total == 0:
        raise AssetNotFound()
    return {"result": assets.items[0]}


def get_random_asset_offset(dataset: models.Dataset) -> int:
    if not dataset.asset_count:
        raise AssetNotFound()
    offset = random.randint(0, dataset.asset_count)
    return offset


@router.get(
    "/{dataset_id}/assets/{asset_hash}",
    response_model=schemas.AssetOut,
    responses={404: {"description": "Asset Not Found"}},
)
def get_asset_of_dataset(
    db: Session = Depends(deps.get_db),
    dataset_id: int = Path(..., example="12"),
    asset_hash: str = Path(..., description="in asset hash format"),
    viz_client: VizClient = Depends(deps.get_viz_client),
    current_user: models.User = Depends(deps.get_current_active_user),
    current_workspace: models.Workspace = Depends(deps.get_current_workspace),
    labels: List = Depends(deps.get_personal_labels),
) -> Any:
    """
    Get asset from specific dataset
    """
    dataset = crud.dataset.get_with_task(db, user_id=current_user.id, id=dataset_id)
    if not dataset:
        raise DatasetNotFound()

    keyword_id_to_name = get_keyword_id_to_name_mapping(labels)
    viz_client.config(
        user_id=current_user.id,
        repo_id=current_workspace.hash,
        branch_id=dataset.task_hash,  # type: ignore
        keyword_id_to_name=keyword_id_to_name,
    )
    asset = viz_client.get_asset(asset_id=asset_hash)
    if not asset:
        raise AssetNotFound()
    return {"result": asset}

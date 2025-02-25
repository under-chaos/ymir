import json
from typing import Any, Dict, List, Optional, Union, Callable
from operator import attrgetter

from fastapi import APIRouter, Depends, Path, Query
from fastapi.logger import logger
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.api.errors.errors import (
    DuplicateTaskError,
    FailedtoCreateTask,
    NoTaskPermission,
    TaskNotFound,
)
from app.config import settings
from app.models import Dataset, Model
from app.models.task import Task, TaskState, TaskType
from app.schemas.task import MergeStrategy
from app.utils.data import groupby
from app.utils.email import send_task_result_email
from app.utils.err import catch_error_and_report
from app.utils.graph import GraphClient
from app.utils.stats import RedisStats
from app.utils.ymir_controller import (
    ControllerClient,
    ControllerRequest,
    ExtraRequestType,
)
from app.utils.ymir_viz import VizClient
from app.utils.class_ids import (
    get_keyword_id_to_name_mapping,
    get_keyword_name_to_id_mapping,
)

router = APIRouter()


@router.get(
    "/", response_model=schemas.TaskOut,
)
def list_tasks(
    db: Session = Depends(deps.get_db),
    name: str = Query(None, description="search by task name"),
    type_: models.task.TaskType = Query(None, alias="type"),
    state: models.task.TaskState = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
    start_time: int = Query(None, description="from this timestamp"),
    end_time: int = Query(None, description="to this timestamp"),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get list of tasks,
    pagination is supported by means of offset and limit
    """
    tasks, total = crud.task.get_multi_tasks(
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
    return {"result": {"total": total, "items": tasks}}


@router.post(
    "/", response_model=schemas.TaskOut,
)
def create_task(
    *,
    db: Session = Depends(deps.get_db),
    task_in: schemas.TaskCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
    current_workspace: models.Workspace = Depends(deps.get_current_workspace),
    controller_client: ControllerClient = Depends(deps.get_controller_client),
    stats_client: RedisStats = Depends(deps.get_stats_client),
    labels: List[str] = Depends(deps.get_personal_labels),
) -> Any:
    """
    Create task

    Note that if you selected multiple datasets, use `strategy` to choose primary one:
     - stop_upon_conflict = 1
     - prefer_newest = 2
     - prefer_oldest = 3
    """
    logger.debug("create task start: %s" % task_in.name)
    task = crud.task.get_by_user_and_name(
        db, user_id=current_user.id, name=task_in.name
    )
    if task:
        raise DuplicateTaskError()

    keyword_name_to_id = get_keyword_name_to_id_mapping(labels)

    # todo: using pydantic to do the normalization
    parameters = normalize_parameters(
        db, task_in.name, task_in.parameters, keyword_name_to_id
    )

    if parameters and task_in.config:
        parameters["config"] = task_in.config

    try:
        task_id = ControllerRequest.gen_task_id(current_user.id)
        resp = controller_client.create_task(
            current_user.id, current_workspace.hash, task_id, task_in.type, parameters,
        )
        logger.info("[create task] controller response: %s", resp)
    except ValueError:
        # todo parse error message
        raise FailedtoCreateTask()

    task = crud.task.create_task(
        db, obj_in=task_in, task_hash=task_id, user_id=current_user.id
    )

    update_stats_for_ref_count(current_user.id, stats_client, task_in)
    logger.info("[create task] created task name: %s" % task_in.name)

    return {"result": task}


def normalize_parameters(
    db: Session,
    name: str,
    parameters: Optional[schemas.TaskParameter],
    keyword_name_to_id: Dict,
) -> Optional[Dict]:
    """
    Normalize task parameters, including:
    - map class_name to class_id
    - map dataset_id to task_hash (which equates branch_id)
    """
    if not parameters:
        return None
    p = dict(parameters)
    normalized = {}  # type: Dict[str, Any]
    normalized["name"] = name
    for k, v in p.items():
        if v is None:
            continue
        if k.endswith("datasets"):
            datasets = crud.dataset.get_multi_by_ids(db, ids=v)
            order_datasets_by_strategy(datasets, parameters.strategy)
            normalized[k] = [dataset.hash for dataset in datasets]
        elif k.endswith("classes"):
            normalized[k] = [keyword_name_to_id[keyword.strip()] for keyword in v]
        elif k == "model_id":
            model = crud.model.get(db, id=v)
            assert model and model.hash
            normalized["model_hash"] = model.hash
        else:
            normalized[k] = v
    return normalized


def order_datasets_by_strategy(
    objects: List[Any], strategy: Optional[MergeStrategy]
) -> None:
    """
    change the order of datasets *in place*
    """
    if not strategy:
        return
    if strategy is MergeStrategy.stop_upon_conflict:
        return
    return objects.sort(
        key=attrgetter("update_datetime"),
        reverse=strategy is MergeStrategy.prefer_newest,
    )


def update_stats_for_ref_count(
    user_id: int, stats_client: RedisStats, task_in: schemas.TaskCreate
) -> None:
    task_type = task_in.type.value
    stats_client.update_task_stats(user_id, task_type)

    if not task_in.parameters:
        return
    parameters = dict(task_in.parameters)
    model_id = parameters.get("model_id")
    if model_id:
        stats_client.update_model_rank(user_id, model_id)
        logger.debug("updated model rank: <model:%s>", model_id)

    dataset_ids = []
    for k, v in parameters.items():
        if k.endswith("datasets") and v:
            dataset_ids += v
    for dataset_id in set(dataset_ids):
        stats_client.update_dataset_rank(user_id, dataset_id)
        logger.debug("updated dataset rank: <dataset:%s>", dataset_id)


@router.delete(
    "/{task_id}",
    response_model=schemas.TaskOut,
    dependencies=[Depends(deps.get_current_active_user)],
    responses={
        400: {"description": "No permission"},
        404: {"description": "Task Not Found"},
    },
)
def delete_task(
    *,
    db: Session = Depends(deps.get_db),
    task_id: int = Path(..., example="12"),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete task
    (soft delete actually)
    """
    task = crud.task.get(db, id=task_id)
    if not task:
        raise TaskNotFound()
    if task.user_id != current_user.id:
        raise NoTaskPermission()
    task = crud.task.soft_remove(db, id=task_id)
    return {"result": task}


@router.get(
    "/{task_id}",
    response_model=schemas.TaskOut,
    response_model_exclude_none=True,
    responses={404: {"description": "Task Not Found"}},
)
def get_task(
    db: Session = Depends(deps.get_db),
    task_id: int = Path(..., example="12"),
    current_user: models.User = Depends(deps.get_current_active_user),
    controller_client: ControllerClient = Depends(deps.get_controller_client),
) -> Any:
    """
    Get verbose information of specific task
    """
    task = crud.task.get_by_user_and_id(db, user_id=current_user.id, id=task_id)
    if not task:
        raise TaskNotFound()
    result = {}
    model = crud.model.get_by_task_id(db, task_id=task_id)
    dataset = crud.dataset.get_by_task_id(db, task_id=task_id)
    if model:
        result["model_id"] = model.id
    if dataset:
        result["dataset_id"] = dataset.id
    if task.state is models.task.TaskState.error:
        req = ControllerRequest(
            ExtraRequestType.get_task_info, task.user_id, args={"task_ids": [task.hash]}
        )
        logger.debug("controller request for get_task_info: %s", req)
        resp = controller_client.send(req)
        info = TaskResultProxy.parse_resp(resp)
        logger.debug("controller response for get_task_info: %s", resp)
        # fixme, update error code when possible
        result["error"] = {"code": -1, "message": info.get("last_error")}
    task.result = result  # type: ignore
    return {"result": task}


@router.patch(
    "/{task_id}",
    response_model=schemas.TaskOut,
    responses={404: {"description": "Task Not Found"}},
)
def update_task_name(
    *,
    db: Session = Depends(deps.get_db),
    task_id: int = Path(..., example="12"),
    task_in: schemas.TaskUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update task name
    """
    task = crud.task.get_by_user_and_name(
        db, user_id=current_user.id, name=task_in.name
    )
    if task:
        raise DuplicateTaskError()

    task = crud.task.get(db, id=task_id)
    if not task:
        raise TaskNotFound()
    task = crud.task.update(db, db_obj=task, obj_in=task_in)
    return {"result": task}


@router.post(
    "/{task_id}/terminate", response_model=schemas.TaskOut,
)
def terminate_task(
    db: Session = Depends(deps.get_db),
    task_id: int = Path(..., example="12"),
    current_user: models.User = Depends(deps.get_current_active_user),
    controller_client: ControllerClient = Depends(deps.get_controller_client),
) -> Any:
    task = crud.task.get(db, id=task_id)
    if not task:
        raise TaskNotFound()
    killable_task_types = [TaskType.training, TaskType.mining, TaskType.label]
    if task.type in killable_task_types:
        controller_client.terminate_task(user_id=current_user.id, target_task=task)
    if task.type is not TaskType.label:
        task = crud.task.update_task_state(
            db, task_id=task.id, new_state=TaskState.error
        )
    return {"result": task}


@router.post(
    "/update_status",
    response_model=schemas.TaskOut,
    dependencies=[Depends(deps.get_current_active_user)],
)
def update_task_status(
    *,
    db: Session = Depends(deps.get_db),
    graph_db: GraphClient = Depends(deps.get_graph_client),
    controller_client: ControllerClient = Depends(deps.get_controller_client),
    viz_client: VizClient = Depends(deps.get_viz_client),
    stats_client: RedisStats = Depends(deps.get_stats_client),
) -> Any:
    """
    Batch update given tasks status
    """
    tasks = crud.task.get_tasks_by_states(
        db, states=[TaskState.pending, TaskState.running], including_deleted=True,
    )
    task_result_proxy = TaskResultProxy(
        db=db,
        graph_db=graph_db,
        controller=controller_client,
        viz=viz_client,
        stats_client=stats_client,
    )
    for user_id, _tasks in groupby(tasks, "user_id"):
        for _task in _tasks:
            task = schemas.Task.from_orm(_task)
            task_result = task_result_proxy.get(task)
            task_result_proxy.save(task, task_result)

    return {"result": {"total": len(tasks), "items": tasks}}


class TaskResultProxy:
    def __init__(
        self,
        *,
        db: Session,
        graph_db: GraphClient,
        controller: ControllerClient,
        stats_client: RedisStats,
        viz: VizClient,
    ):
        self.db = db
        self.graph_db = graph_db
        self.controller = controller
        self.stats_client = stats_client
        self.viz = viz

    def get(self, task: schemas.Task) -> Dict:
        req = ControllerRequest(
            ExtraRequestType.get_task_info, task.user_id, args={"task_ids": [task.hash]}
        )
        logger.info("controller request for get_task_info: %s", req)
        resp = self.controller.send(req)
        logger.info("controller response for get_task_info: %s", resp)
        task_info = self.parse_resp(resp)
        return task_info

    @catch_error_and_report
    def save(self, task: schemas.Task, task_result: Dict) -> None:
        if not task_result or task_result["state"] == TaskState.unknown:
            logger.info("skip invalid task_result: %s", task_result)
            return

        if task_result["state"] == TaskState.done:
            self.handle_finished_task(task)

        if (
            task.type is TaskType.import_data
            and task_result["state"] == TaskState.error
        ):
            # fixme:
            #  parse error msg of failed to import_task
            #  to get ignored_keywords
            self.handle_failed_import_task(task, task_result)

        logger.debug("task progress used to be %s", task)
        updated_task = self.update_task_progress(task, task_result)
        logger.debug("task progress updated to %s", updated_task)

        if task_result["state"] in (TaskState.error, TaskState.done):
            logger.debug("Sending notification for task: %s", task)
            self.send_notification(task, task_result)

    @staticmethod
    def parse_resp(result: Dict) -> Dict:
        info = list(result["resp_get_task_info"]["task_infos"].values())[0]
        return info

    @catch_error_and_report
    def send_notification(self, task: schemas.Task, task_info: Dict) -> None:
        creator = crud.user.get(self.db, id=task.user_id)
        if not (settings.EMAILS_ENABLED and creator and creator.email):
            return
        email = creator.email
        send_task_result_email(
            email,
            task.id,
            task.name,
            task.type.name,
            task_info["state"] == TaskState.done,
        )

    def handle_finished_task(self, task: schemas.Task) -> None:
        if task.type is TaskType.training:
            model = self.add_new_model_if_not_exist(task)
            self.stats_client.update_model_rank(task.user_id, model.id)
            keywords = schemas.model.extract_keywords(task.parameters)
            if model.map and keywords:
                self.stats_client.update_keyword_wise_model_rank(
                    task.user_id, model.id, float(model.map), keywords
                )
            logger.debug("task result(new model): %s", model)
            node = schemas.Model.from_orm(model)  # type: ignore
        elif task.type in [TaskType.mining, TaskType.label, TaskType.filter]:
            dataset = self.add_new_dataset_if_not_exist(task)
            logger.debug("task result(new dataset): %s", dataset)
            self.stats_client.update_dataset_rank(task.user_id, dataset.id)
            logger.info("task result(dataset %s) ref_count initialized", dataset.id)
            node = schemas.Dataset.from_orm(dataset)  # type: ignore
        elif task.type in [TaskType.import_data, TaskType.copy_data]:
            dataset = self.update_dataset(task)  # type: ignore
            logger.debug("task result(updated dataset): %s", dataset)
            self.stats_client.update_dataset_rank(task.user_id, dataset.id)
            logger.info("task result(dataset %s) ref_count initialized", dataset.id)
            node = schemas.Dataset.from_orm(dataset)  # type: ignore
        else:
            logger.info("nothing to do for task: %s" % task)
            return

        parents = self.get_parent_nodes(task.parameters)  # type: ignore
        self.update_graph(parents=parents, node=node, task=task)
        logger.debug(
            "[graph] updated with parents: %s, node: %s and task: %s",
            parents,
            node,
            task,
        )

    def handle_failed_import_task(self, task: schemas.Task, task_result: Dict) -> None:
        # makeup data for failed dataset
        dataset_info = {
            "keywords": [],
            "ignored_keywords": self._parse_ignored_keywords(task_result.get("state_message")),
            "items": 0,
            "total": 0,
        }
        logger.debug("[failed task] update dataset with %s", dataset_info)
        dataset = self.update_dataset(task, dataset_info)
        logger.debug("[failed task] added ignored_keywords to dataset: %s", dataset)

    def _parse_ignored_keywords(self, error_message: Optional[str]) -> List[str]:
        if not error_message:
            return []
        try:
            ignored_keywords = list(json.loads(error_message).keys())
        except Exception:
            ignored_keywords = []
        return ignored_keywords

    def add_new_dataset_if_not_exist(self, task: schemas.Task) -> Dataset:
        dataset = crud.dataset.get_by_hash(self.db, hash_=task.hash)
        if dataset:
            # dataset already added before
            return dataset

        dataset_info = self.get_dataset_info(task.user_id, task.hash)
        dataset_in = schemas.DatasetCreate(
            name=get_default_record_name(task.hash, task.name),
            hash=task.hash,
            type=task.type,
            user_id=task.user_id,
            task_id=task.id,
            predicates=self._extract_keywords(dataset_info),
            asset_count=dataset_info["total"],
            keyword_count=len(dataset_info["keywords"]),
        )
        dataset = crud.dataset.create(self.db, obj_in=dataset_in)
        return dataset

    def update_dataset(self, task: schemas.Task, dataset_info: Optional[Dict] = None) -> Optional[Dataset]:
        dataset = crud.dataset.get_by_hash(self.db, hash_=task.hash)
        if not dataset:
            return dataset

        dataset_info = dataset_info or self.get_dataset_info(task.user_id, task.hash)
        dataset_in = schemas.DatasetUpdate(
            predicates=self._extract_keywords(dataset_info),
            asset_count=dataset_info["total"],
            keyword_count=len(dataset_info["keywords"]),
        )
        updated = crud.dataset.update(self.db, db_obj=dataset, obj_in=dataset_in)
        return updated

    def _extract_keywords(self, dataset_info: Dict) -> str:
        return json.dumps(
            {
                "keywords": dataset_info["keywords"],
                "ignored_keywords": dataset_info["ignored_keywords"],
            }
        )

    def add_new_model_if_not_exist(self, task: schemas.Task) -> Model:
        self.viz.config(user_id=task.user_id, branch_id=task.hash)
        model_info = self.viz.get_model()
        if not model_info:
            raise ValueError("model not ready yet")

        model = crud.model.get_by_hash(self.db, hash_=model_info["hash"])
        if model:
            # model already added before
            return model

        model_in = schemas.ModelCreate(
            name=get_default_record_name(task.hash, task.name),
            hash=model_info["hash"],
            map=model_info["map"],
            user_id=task.user_id,
            task_id=task.id,
        )
        model = crud.model.create(self.db, obj_in=model_in)
        return model

    def get_dataset_info(self, user_id: int, task_hash: str) -> Dict:
        labels = self.controller.get_labels_of_user(user_id)
        keyword_id_to_name = get_keyword_id_to_name_mapping(labels)
        self.viz.config(
            user_id=user_id, branch_id=task_hash, keyword_id_to_name=keyword_id_to_name
        )

        assets = self.viz.get_assets()
        result = {
            "keywords": list(assets.keywords.keys()),
            "ignored_keywords": list(assets.ignored_keywords.keys()),
            "items": assets.items,
            "total": assets.total,
        }
        return result

    def update_task_progress(
        self, task: schemas.Task, task_info: Dict
    ) -> Optional[Task]:
        task_obj = crud.task.get(self.db, id=task.id)
        if not task_obj:
            return task_obj
        progress_update = {
            "state": TaskState(task_info["state"]),
            "progress": int(task_info["percent"] * 100)
            if "percent" in task_info
            else 0,
        }
        updated_task = crud.task.update(
            self.db, db_obj=task_obj, obj_in=progress_update
        )
        return updated_task

    def get_parent_nodes(self, parameters: Dict) -> List:
        """
        Parse task parameters to get input datasets and models for a task
        """
        dataset_ids = set()  # type: set
        for k, v in parameters.items():
            if k.endswith("datasets") and v:
                dataset_ids = dataset_ids.union(v)
        datasets = crud.dataset.get_multi_by_ids(self.db, ids=list(dataset_ids))
        datasets = [schemas.Dataset.from_orm(i) for i in datasets]  # type: ignore

        models = []
        model_id = parameters.get("model_id")
        if model_id:
            model = crud.model.get(self.db, id=model_id)
            if model:
                models = [schemas.Model.from_orm(model)]
        return datasets + models  # type: ignore

    @staticmethod
    def convert_to_graph_node(
        node: Union[schemas.Model, schemas.Dataset, schemas.Task]
    ) -> Dict:
        required_fields = ["hash", "id", "name", "type"]
        graph_node = {k: v for k, v in node.dict().items() if k in required_fields}
        graph_node["label"] = node.__repr_name__()
        if graph_node.get("type"):
            graph_node["type"] = graph_node["type"].value
        return graph_node

    def update_graph(
        self,
        *,
        parents: Optional[List] = None,
        node: Union[schemas.Dataset, schemas.Model],
        task: Optional[schemas.Task] = None,
    ) -> None:
        self.graph_db.user_id = task.user_id  # type: ignore
        graph_node = self.convert_to_graph_node(node)
        if parents and task:
            graph_task = self.convert_to_graph_node(task)
            for parent in parents:
                graph_parent = self.convert_to_graph_node(parent)
                self.graph_db.add_relationship(graph_parent, graph_node, graph_task)
        else:
            self.graph_db.add_node(graph_node)


def get_default_record_name(task_hash: str, task_name: str) -> str:
    return f"{task_name}_{task_hash[-6:]}"

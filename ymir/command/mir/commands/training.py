import argparse
import datetime
import logging
import os
import shutil
import subprocess
import tarfile
from typing import Any, List, Optional, Set, Tuple

import yaml

from mir.commands import base
from mir.protos import mir_command_pb2 as mirpb
from mir.tools import checker, class_ids, data_exporter, hash_utils, mir_storage_ops, revs_parser
from mir.tools.code import MirCode
from mir.tools.phase_logger import phase_logger_in_out


def _process_model_storage(out_root: str, config_file_path: str, model_upload_location: str,
                           ymir_info: dict) -> Tuple[str, float]:
    models = _find_models(os.path.join(out_root, "models"))
    model_paths = models[0]
    model_mAP = models[1]
    if not model_paths:
        raise ValueError("can not find models")
    tar_path = os.path.join(out_root, "models.tar.gz")
    _pack_models_and_config(model_paths=model_paths,
                            config_file_path=config_file_path,
                            ymir_info=dict(**ymir_info, mAP=model_mAP),
                            dest_path=tar_path)
    model_sha1 = hash_utils.sha1sum_for_file(tar_path)

    dest_path = os.path.join(model_upload_location, model_sha1)
    _upload_model_pack(tar_path, dest_path)
    os.remove(tar_path)

    return model_sha1, model_mAP


def _find_models(model_root: str) -> Tuple[List[str], float]:
    """
    find models in `model_root`, and returns model names and mAP

    Args:
        model_root (str): model root

    Returns:
        Tuple[List[str], float]: list of model names and map
    """
    model_names = []
    model_mAP = 0.0

    with open(os.path.join(model_root, "result.yaml"), "r") as f:
        yaml_obj = yaml.safe_load(f.read())
        model_names = yaml_obj["model"]
        model_mAP = float(yaml_obj["map"])

    return ([os.path.join(model_root, name) for name in model_names], model_mAP)


def _pack_models_and_config(model_paths: List[str], config_file_path: str, ymir_info: dict, dest_path: str) -> bool:
    if not model_paths or not dest_path:
        raise ValueError("invalid model_paths or dest_path")

    with tarfile.open(dest_path, "w:gz") as dest_tar_gz:
        logging.info("packing models and configs")
        for model_path in model_paths:
            logging.info(f"    packing {model_path} -> {os.path.basename(model_path)}")
            dest_tar_gz.add(model_path, os.path.basename(model_path))
        logging.info(f"    packing {config_file_path} -> config.yaml")
        dest_tar_gz.add(config_file_path, 'config.yaml')

        # pack ymir-info.yaml
        ymir_info_file_name = 'ymir-info.yaml'
        ymir_info_file_path = os.path.join(os.path.dirname(config_file_path), ymir_info_file_name)
        with open(ymir_info_file_path, 'w') as f:
            f.write(yaml.dump(ymir_info if ymir_info else {}))
        logging.info(f"    packing {ymir_info_file_path} -> {ymir_info_file_name}")
        dest_tar_gz.add(ymir_info_file_path, ymir_info_file_name)
    return True


def _upload_model_pack(model_pack_path: str, dest_path: str) -> bool:
    if not model_pack_path or not dest_path:
        raise ValueError("invalid model_pack_path or dest_path")

    shutil.copyfile(model_pack_path, dest_path)
    return True


def _update_mir_tasks(mir_root: str, base_branch: str, dst_branch: str, task_id: str, model_sha1: str,
                      mAP: float) -> None:
    """
    add a new mir single task into mir_tasks from branch base_branch, and save it to a new branch: dst_branch
    """
    task = mirpb.Task()
    task.type = mirpb.TaskTypeTraining
    task.name = "training done"
    task.task_id = task_id
    task.timestamp = int(datetime.datetime.now().timestamp())
    task.model.model_hash = model_sha1
    task.model.mean_average_precision = mAP

    mir_tasks: mirpb.MirTasks = mir_storage_ops.MirStorageOps.load_single(mir_root=mir_root,
                                                                          mir_branch=base_branch,
                                                                          ms=mirpb.MirStorage.MIR_TASKS)
    mir_storage_ops.add_mir_task(mir_tasks, task)
    mir_storage_ops.MirStorageOps.save_and_commit(mir_root=mir_root,
                                                  mir_branch=dst_branch,
                                                  his_branch=base_branch,
                                                  mir_datas={mirpb.MirStorage.MIR_TASKS: mir_tasks},
                                                  commit_message=task_id)

    logging.info("task id: {}, model hash: {}, mAP: {}".format(task_id, model_sha1, mAP))


# add this function for mock unit test.
def _run_train_cmd(cmd: str) -> int:
    logging.info("training with cmd: {}".format(cmd))
    subprocess.run(cmd.split(" "), check=True)  # run and wait, if non-zero value returned, raise

    return MirCode.RC_OK


def _generate_config(config: Any, out_config_path: str, task_id: str) -> None:
    config["task_id"] = task_id

    logging.debug("config: {}".format(config))

    with open(out_config_path, "w") as f:
        yaml.dump(config, f)


class CmdTrain(base.BaseCommand):
    def run(self) -> int:
        logging.debug("command train: %s", self.args)

        return CmdTrain.run_with_args(work_dir=self.args.work_dir,
                                      model_upload_location=self.args.model_path,
                                      src_revs=self.args.src_revs,
                                      dst_rev=self.args.dst_rev,
                                      mir_root=self.args.mir_root,
                                      media_location=self.args.media_location,
                                      executor=self.args.executor,
                                      executor_instance=self.args.executor_instance,
                                      config_file=self.args.config_file)

    @staticmethod
    @phase_logger_in_out
    def run_with_args(work_dir: str,
                      model_upload_location: str,
                      executor: str,
                      executor_instance: str,
                      src_revs: str,
                      dst_rev: str,
                      config_file: Optional[str],
                      mir_root: str = '.',
                      media_location: str = '') -> int:

        if not model_upload_location:
            logging.error("empty --model-location, abort")
            return MirCode.RC_CMD_INVALID_ARGS
        if not src_revs:
            logging.error('empty --src-revs, abort')
            return MirCode.RC_CMD_INVALID_ARGS
        src_typ_rev_tid = revs_parser.parse_single_arg_rev(src_revs)
        if checker.check_src_revs(src_typ_rev_tid) != MirCode.RC_OK:
            return MirCode.RC_CMD_INVALID_ARGS
        dst_typ_rev_tid = revs_parser.parse_single_arg_rev(dst_rev)
        if checker.check_dst_rev(dst_typ_rev_tid) != MirCode.RC_OK:
            return MirCode.RC_CMD_INVALID_ARGS
        if not work_dir:
            logging.error("empty work_dir, abort")
            return MirCode.RC_CMD_INVALID_ARGS
        if not config_file:
            logging.warning('empty --config-file, abort')
            return MirCode.RC_CMD_INVALID_ARGS
        if not os.path.isfile(config_file):
            logging.error(f"invalid --config-file {config_file}, not a file, abort")
            return MirCode.RC_CMD_INVALID_ARGS

        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
        if 'class_names' not in config:
            logging.error(f"no class_names in config file: {config_file}, abort")
            return MirCode.RC_CMD_INVALID_ARGS

        class_names = config['class_names']
        if not class_names:
            logging.error(f"empty class_names in config file: {config_file}, abort")
            return MirCode.RC_CMD_INVALID_ARGS
        if len(set(class_names)) != len(class_names):
            logging.error(f"dumplicate class names in class_names: {class_names}, abort")
            return MirCode.RC_CMD_INVALID_ARGS

        return_code = checker.check(mir_root,
                                    [checker.Prerequisites.IS_INSIDE_MIR_REPO, checker.Prerequisites.HAVE_LABELS])
        if return_code != MirCode.RC_OK:
            return return_code

        task_id = dst_typ_rev_tid.tid
        if not executor_instance:
            executor_instance = f"default-training-{task_id}"

        # get train_ids, val_ids, test_ids
        train_ids = set()  # type: Set[str]
        val_ids = set()  # type: Set[str]
        test_ids = set()  # type: Set[str]
        unused_ids = set()  # type: Set[str]
        mir_datas = mir_storage_ops.MirStorageOps.load(mir_root=mir_root,
                                                       mir_branch=src_typ_rev_tid.rev,
                                                       mir_storages=[mirpb.MirStorage.MIR_METADATAS])
        mir_metadatas: mirpb.MirMetadatas = mir_datas[mirpb.MirStorage.MIR_METADATAS]
        for asset_id, asset_attr in mir_metadatas.attributes.items():
            if asset_attr.tvt_type == mirpb.TvtTypeTraining:
                train_ids.add(asset_id)
            elif asset_attr.tvt_type == mirpb.TvtTypeValidation:
                val_ids.add(asset_id)
            elif asset_attr.tvt_type == mirpb.TvtTypeTest:
                test_ids.add(asset_id)
            else:
                unused_ids.add(asset_id)
        if not train_ids:
            logging.error("no training set; abort")
            return MirCode.RC_CMD_INVALID_ARGS
        if not val_ids:
            logging.error("no validation set; abort")
            return MirCode.RC_CMD_INVALID_ARGS

        if not unused_ids:
            logging.info(f"training: {len(train_ids)}, validation: {len(val_ids)}, test: {len(test_ids)}")
        else:
            logging.warning(f"training: {len(train_ids)}, validation: {len(val_ids)}, test: {len(test_ids)}, "
                            f"unused: {len(unused_ids)}")

        # export
        logging.info("exporting assets")
        os.makedirs(work_dir, exist_ok=True)
        work_dir_in = os.path.join(work_dir, "in")
        work_dir_out = os.path.join(work_dir, "out")
        os.makedirs(work_dir_in, exist_ok=True)
        os.makedirs(work_dir_out, exist_ok=True)

        # type names to type ids
        # ['cat', 'person'] -> [4, 2]
        cls_mgr = class_ids.ClassIdManager(mir_root=mir_root)
        type_ids_list = cls_mgr.id_for_names(class_names)
        if not type_ids_list:
            logging.info(f"type ids empty, please check config file: {config_file}")
            return MirCode.RC_CMD_INVALID_ARGS
        type_id_idx_mapping = {type_id: index for (index, type_id) in enumerate(type_ids_list)}

        # export train set
        work_dir_in_train = os.path.join(work_dir_in, 'train')
        if os.path.isdir(work_dir_in_train):
            shutil.rmtree(work_dir_in_train)
        data_exporter.export(mir_root=mir_root,
                             assets_location=media_location,
                             class_type_ids=type_id_idx_mapping,
                             asset_ids=train_ids,
                             asset_dir=work_dir_in_train,
                             annotation_dir=work_dir_in_train,
                             need_ext=True,
                             need_id_sub_folder=False,
                             base_branch=src_typ_rev_tid.rev,
                             format_type=data_exporter.ExportFormat.EXPORT_FORMAT_ARK,
                             index_file_path=os.path.join(work_dir_in_train, 'index.tsv'),
                             index_prefix='/in/train')

        # export validation set
        work_dir_in_val = os.path.join(work_dir_in, 'val')
        if os.path.isdir(work_dir_in_val):
            shutil.rmtree(work_dir_in_val)
        data_exporter.export(mir_root=mir_root,
                             assets_location=media_location,
                             class_type_ids=type_id_idx_mapping,
                             asset_ids=val_ids,
                             asset_dir=work_dir_in_val,
                             annotation_dir=work_dir_in_val,
                             need_ext=True,
                             need_id_sub_folder=False,
                             base_branch=src_typ_rev_tid.rev,
                             format_type=data_exporter.ExportFormat.EXPORT_FORMAT_ARK,
                             index_file_path=os.path.join(work_dir_in_val, 'index.tsv'),
                             index_prefix='/in/val')

        # export test set (if we have)
        if test_ids:
            work_dir_in_test = os.path.join(work_dir_in, 'test')
            if os.path.isdir(work_dir_in_test):
                shutil.rmtree(work_dir_in_test)
            data_exporter.export(mir_root=mir_root,
                                 assets_location=media_location,
                                 class_type_ids=type_id_idx_mapping,
                                 asset_ids=test_ids,
                                 asset_dir=work_dir_in_test,
                                 annotation_dir=work_dir_in_test,
                                 need_ext=True,
                                 need_id_sub_folder=False,
                                 base_branch=src_typ_rev_tid.rev,
                                 format_type=data_exporter.ExportFormat.EXPORT_FORMAT_ARK,
                                 index_file_path=os.path.join(work_dir_in_test, 'index.tsv'),
                                 index_prefix='/in/test')

        logging.info("starting train docker container")

        # generate configs
        out_config_path = os.path.join(work_dir_in, "config.yaml")
        _generate_config(config=config, out_config_path=out_config_path, task_id=task_id)

        # start train docker and wait
        path_binds = []
        path_binds.append(f"-v {work_dir_in}:/in")
        path_binds.append(f"-v {work_dir_out}:/out")
        joint_path_binds = " ".join(path_binds)
        shm_size = _get_shm_size(config_file)
        cmd = (f"nvidia-docker run --rm --shm-size={shm_size} {joint_path_binds} --user {os.getuid()}:{os.getgid()} "
               f"--name {executor_instance} {executor}")

        ret = _run_train_cmd(cmd)
        if ret != MirCode.RC_OK:
            return ret

        # save model
        logging.info("saving models")
        model_sha1, model_mAP = _process_model_storage(out_root=work_dir_out,
                                                       config_file_path=out_config_path,
                                                       model_upload_location=model_upload_location,
                                                       ymir_info={
                                                           'src_revs': src_revs,
                                                           'dst_rev': dst_rev,
                                                           'executor': executor
                                                       })
        # update metadatas and task with finish state and model hash
        logging.info("creating task")
        _update_mir_tasks(mir_root=mir_root,
                          base_branch=src_typ_rev_tid.rev,
                          dst_branch=dst_typ_rev_tid.rev,
                          task_id=task_id,
                          model_sha1=model_sha1,
                          mAP=model_mAP)

        logging.info("training done")

        return MirCode.RC_OK


def _get_shm_size(config_file_path: str) -> str:
    with open(config_file_path, 'r') as f:
        config = yaml.safe_load(f.read())
    if 'shm_size' not in config:
        return '16G'
    return config['shm_size']


def bind_to_subparsers(subparsers: argparse._SubParsersAction,
                       parent_parser: argparse.ArgumentParser) -> None:  # pragma: no cover
    train_arg_parser = subparsers.add_parser("train",
                                             parents=[parent_parser],
                                             description="use this command to train current workspace",
                                             help="train current workspace")
    train_arg_parser.add_argument("--model-location",
                                  required=True,
                                  dest="model_path",
                                  type=str,
                                  help="storage place (upload location) to store packed model")
    train_arg_parser.add_argument("--media-location",
                                  required=True,
                                  dest="media_location",
                                  type=str,
                                  help="media storage location for models")
    train_arg_parser.add_argument("-w", required=True, dest="work_dir", type=str, help="work place for training")
    train_arg_parser.add_argument("--executor",
                                  required=True,
                                  dest="executor",
                                  type=str,
                                  help="docker image name for training")
    train_arg_parser.add_argument('--executor-instance',
                                  required=False,
                                  dest='executor_instance',
                                  type=str,
                                  help='docker container name for training')
    train_arg_parser.add_argument("--src-revs",
                                  dest="src_revs",
                                  type=str,
                                  required=True,
                                  help="rev@bid: source rev and base task id")
    train_arg_parser.add_argument("--dst-rev",
                                  dest="dst_rev",
                                  type=str,
                                  required=True,
                                  help="rev@tid: destination branch name and task id")
    train_arg_parser.add_argument("--config-file",
                                  dest="config_file",
                                  type=str,
                                  required=True,
                                  help="path to executor config file")
    train_arg_parser.set_defaults(func=CmdTrain)

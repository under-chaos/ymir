import time
from typing import List, Dict, Set

from pynvml import nvmlInit, nvmlDeviceGetCount, nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo, nvmlShutdown

from controller.config import GPU_LOCKING_SET, GPU_LOCK_MINUTES, GPU_USAGE_THRESHOLD
from controller.utils.redis import rds


class GPUInfo:
    @staticmethod
    def get_gpus_info() -> Dict:
        gpu_info = dict()
        nvmlInit()
        for i in range(nvmlDeviceGetCount()):
            handle = nvmlDeviceGetHandleByIndex(i)
            gpu_mem_info = nvmlDeviceGetMemoryInfo(handle)
            free_percent = gpu_mem_info.free / gpu_mem_info.total
            gpu_info[str(i)] = free_percent
        nvmlShutdown()

        return gpu_info

    @staticmethod
    def get_free_gpus() -> Set:
        gpus_info = GPUInfo.get_gpus_info()
        runtime_free_gpus = {i for i, free_percent in gpus_info.items() if free_percent > GPU_USAGE_THRESHOLD}

        return runtime_free_gpus

    @classmethod
    def get_locked_gpus(cls) -> Set:
        # lock gpu about 30 minutes for loading
        cut_off_time = time.time() - 60 * GPU_LOCK_MINUTES
        rds.zremrangebyscore(GPU_LOCKING_SET, cut_off_time)
        locked_gpus = rds.zrange(GPU_LOCKING_SET)

        return set(locked_gpus)

    @classmethod
    def add_locked_gpus(cls, gpus: List[str]) -> None:
        gpu_mapping = {gpu: time.time() for gpu in gpus}
        rds.zadd(GPU_LOCKING_SET, gpu_mapping)

    @classmethod
    def get_available_gpus(cls) -> List:
        runtime_free_gpus = GPUInfo.get_free_gpus()
        locked_gpus = cls.get_locked_gpus()
        ava_gpus = runtime_free_gpus - locked_gpus

        return list(ava_gpus)

    @classmethod
    def find_gpu_ids_by_config(cls, gpu_count: int, lock_gpu: bool = False) -> str:
        free_gpus = cls.get_available_gpus()
        if len(free_gpus) < gpu_count:
            return ""
        gpus = free_gpus[0:gpu_count]
        if lock_gpu:
            cls.add_locked_gpus(gpus)

        return ",".join(gpus)

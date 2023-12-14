import pytest
from distributed import Scheduler, Worker
from distributed.utils_test import gen_test, loop, cleanup, loop_in_thread
from distributed_heterogeneous import HeterogeneousCluster


@gen_test()
async def test_basic(loop):
    scheduler = {"cls": Scheduler, "options": {"dashboard_address": ":0"}}
    workers = {
        "low-memory-pool": {"cls": Worker, "options": {"memory_limit": "1GB"}},
    }
    cluster = HeterogeneousCluster(
        scheduler=scheduler,
        worker=workers,
        shutdown_on_close=True,
        asynchronous=True,
        loop=loop,
    )
    cluster.scale(3, pool="low-memory-pool")
    cluster.scale(0, pool="low-memory-pool")
    cluster.worker_spec
    cluster.close()

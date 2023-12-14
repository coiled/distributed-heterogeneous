import asyncio
import time

import pytest
from distributed import Scheduler, Worker
from distributed.utils_test import gen_test

from distributed_heterogeneous import HeterogeneousCluster


@gen_test()
async def test_multiple_pools_async():
    scheduler = {"cls": Scheduler, "options": {"dashboard_address": ":0"}}
    workers = {
        "low-memory-pool": {"cls": Worker, "options": {"memory_limit": "1GB"}},
        "high-memory-pool": {"cls": Worker, "options": {"memory_limit": "3GB"}},
    }
    cluster = await HeterogeneousCluster(
        scheduler=scheduler,
        worker=workers,
        asynchronous=True,
    )
    assert cluster.asynchronous
    cluster.scale(2, pool="low-memory-pool")
    cluster.scale(1, pool="high-memory-pool")
    await cluster.wait_for_workers(3)

    cluster.scale(0, pool="low-memory-pool")
    while len(cluster.scheduler_info["workers"]) != 1:
        await asyncio.sleep(0.1)

    cluster.scale(0, pool="high-memory-pool")

    while cluster.scheduler_info["workers"]:
        await asyncio.sleep(0.1)
    await cluster.close()


def test_basic_sync():
    scheduler = {"cls": Scheduler, "options": {"dashboard_address": ":0"}}
    workers = {
        "low-memory-pool": {"cls": Worker, "options": {"memory_limit": "1GB"}},
    }
    cluster = HeterogeneousCluster(
        scheduler=scheduler,
        worker=workers,
    )
    cluster.scale(3, pool="low-memory-pool")
    cluster.wait_for_workers(3)
    cluster.scale(0, pool="low-memory-pool")

    assert len(cluster.worker_spec) == 0
    while cluster.scheduler_info["workers"]:
        time.sleep(0.1)
    cluster.close()

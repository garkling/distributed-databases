import os
import sys
import uuid
from contextlib import contextmanager

from hazelcast.client import HazelcastClient
from dotenv import load_dotenv

sys.path.append('..')
from timer import measure
from logger import get_logger


load_dotenv()
HZ_CLUSTER_MEMBERS = os.environ['HZ_CLUSTER_MEMBERS'].split(',')

logger = get_logger('hazelcast', fmt="[%(asctime)s][%(levelname)s] - %(name)s -- %(message)s")


@contextmanager
def get_conn():
    client = HazelcastClient(
        cluster_members=HZ_CLUSTER_MEMBERS,
        use_public_ip=True,
        smart_routing=False
    )

    yield client

    client.shutdown()


@measure("IMap non-blocking counter process")
def map_non_blocking_counter_increment(map_name, key, n):
    with get_conn() as client:
        dm = client.get_map(map_name).blocking()
        for _ in range(n):
            counter = dm.get(key)
            dm.put(key, counter + 1)


@measure("IMap pessimistic locking counter process")
def map_pessimistic_locking_counter_increment(map_name, key, n):
    with get_conn() as client:
        dm = client.get_map(map_name).blocking()
        for _ in range(n):
            dm.lock(key)
            try:
                counter = dm.get(key)
                dm.put(key, counter + 1)
            finally:
                dm.unlock(key)


@measure("IMap optimistic locking counter process")
def map_optimistic_locking_counter_increment(map_name, key, n):
    with get_conn() as client:
        dm = client.get_map(map_name).blocking()
        for _ in range(n):
            while True:
                counter = dm.get(key)
                if dm.replace_if_same(key, counter, counter + 1):
                    break


@measure("IAtomicLong counter process")
def atomic_long_counter(name, n):
    with get_conn() as client:
        counter = client.cp_subsystem.get_atomic_long(name).blocking()
        for _ in range(n):
            counter.increment_and_get()


def get_map_counter_result(map_name, key):
    with get_conn() as client:
        dm = client.get_map(map_name).blocking()
        logger.info(f'IMap counter value - {dm.get(key)}')


def init_map_counter():
    map_name, key = 'counter_map', 'counter'
    with get_conn() as client:
        dm = client.get_map(map_name).blocking()
        dm.put(key, 0)

    return map_name, key


def generate_atomic_long_name():
    return uuid.uuid4().hex,


def destroy_atomic_counter(name):
    with get_conn() as client:
        counter = client.cp_subsystem.get_atomic_long(name).blocking()
        logger.info(f"IAtomicLong counter value - {counter.get()}")
        counter.destroy()


methods = {
    'imap_non_blocking': dict(method=map_non_blocking_counter_increment, pre=init_map_counter, post=get_map_counter_result),
    'imap_pes_lock': dict(method=map_pessimistic_locking_counter_increment, pre=init_map_counter, post=get_map_counter_result),
    'imap_opt_lock': dict(method=map_optimistic_locking_counter_increment, pre=init_map_counter, post=get_map_counter_result),
    'iatomiclong': dict(method=atomic_long_counter, pre=generate_atomic_long_name, post=destroy_atomic_counter)
}


if __name__ == '__main__':
    import time
    import argparse
    from executor import ThreadExecutor

    parser = argparse.ArgumentParser(description='Hazelcast counter update methods')
    parser.add_argument('--method', type=str, choices=methods, action='append', dest='methods', required=False,
                        help='Method of incrementing the counter from multiple connections')
    parser.add_argument('--connections', type=int, default=10, required=False,
                        help="Number of simultaneous `connections` (thread workers)")
    parser.add_argument('--iters', type=int, default=10_000, required=False,
                        help="Number of counter increment requests from each `connection`")

    args = parser.parse_args()

    for method in (args.methods or methods):
        executor = ThreadExecutor(**methods[method], workers=args.connections)
        executor.run(args.iters)
        time.sleep(5)

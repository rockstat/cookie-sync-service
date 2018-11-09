from prodict import Prodict
from aioredis.pool import ConnectionsPool


class Partner:
    init: str
    sync: str


class State(Prodict):
    redis_pool: ConnectionsPool
    partners: Prodict

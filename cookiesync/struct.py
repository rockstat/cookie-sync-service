from prodict import Prodict
from aioredis.pool import ConnectionsPool


class Partner:
    init: str
    sync: str


class State(Prodict):
    redis_pool: ConnectionsPool
    partners: Prodict

    def get_partner(self, partner) -> Partner:
        if partner:
            return self.partners.get(partner, None)

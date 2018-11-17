from prodict import Prodict
from aioredis.pool import ConnectionsPool
from collections import namedtuple


class ServiceId(namedtuple("ServiceId", ["service", "id"])):
    __slots__ = ()

    def __str__(self):
        return self.service + ':' + str(self.id)

    @classmethod
    def from_str(cls, value):
        return cls(*value.split(':'))


class Partner:
    init: str
    sync: str


class State(Prodict):
    redis_pool: ConnectionsPool
    partners: Prodict

    def get_partner(self, partner) -> Partner:
        if partner:
            return self.partners.get(partner, None)

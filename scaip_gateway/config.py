from dataclasses import dataclass
from typing import Optional, FrozenSet
from functools import lru_cache
from enum import Enum


class Transport(Enum):
    UDP = "udp"
    TCP = "tcp"
    TLS = "tls"


@dataclass(frozen=True, eq=True)
class AlarmReceivingCenterUser:
    username: str
    password: str


@dataclass(frozen=True, eq=True)
class AlarmReceivingCenter:
    name: str
    hostname: str
    port: int
    username: Optional[str] = None
    transport: Transport = Transport.UDP
    user: Optional[AlarmReceivingCenterUser] = None


@dataclass(frozen=True, eq=True)
class Configuration:
    arcs: FrozenSet[AlarmReceivingCenter]

    def __post_init__(self):
        if len(self.arcs) != len(set(arc.name for arc in self.arcs)):
            raise ValueError("dupplicated ARC name provided")

    @lru_cache(maxsize=None)
    def get_arc_config(self, arc_name: str) -> AlarmReceivingCenter:
        return [arc for arc in self.arcs if arc.name == arc_name][0]
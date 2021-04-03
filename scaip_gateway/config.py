from dataclasses import dataclass
from typing import Optional, FrozenSet
from functools import lru_cache

@dataclass(frozen=True, eq=True)
class SipConfiguration:
    hostname: str
    port: str
    username: str
    password: Optional[str] = None
    register: bool = False

@dataclass(frozen=True, eq=True)
class AlarmReceivingCenter:
    name: str
    hostname: str
    port: str
    username: str
    password: str

@dataclass(frozen=True, eq=True)
class Configuration:
    sip: SipConfiguration
    arcs: FrozenSet[AlarmReceivingCenter]

    def __post_init__(self):
        if len(self.arcs) != len(set(arc.name for arc in self.arcs)):
            raise ValueError("dupplicated ARC name provided")

    @lru_cache(maxsize=None)
    def get_arc_config(self, arc_name: str) -> AlarmReceivingCenter:
        return [arc for arc in self.arcs if arc.name == arc_name][0]
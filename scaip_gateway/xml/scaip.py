from dataclasses import dataclass, field
from typing import List, Optional
from xsdata.models.datatype import XmlDateTime


@dataclass
class Mrq:
    class Meta:
        name = "mrq"

    ref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
            "pattern": r"[0-9a-zA-Z]{1,16}",
        }
    )
    ver: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "pattern": r"[0-9]{2}\.[0-9]{2}",
        }
    )
    sco: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "pattern": r"[1-3]{1}",
        }
    )
    cha: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "pattern": r"[0-9]{1}",
        }
    )
    mty: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "pattern": r"(ME)|(RE)|(IN)|(PI)",
        }
    )
    hbo: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "pattern": r"[0-3]{1}",
        }
    )
    cid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
            "pattern": r"[0-9]{1,16}",
        }
    )
    dty: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
            "pattern": r"[0-9]{1,4}",
        }
    )
    did: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "min_length": 1,
            "max_length": 8,
        }
    )
    dco: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "pattern": r"[0-9]{1,3}",
        }
    )
    dte: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "min_length": 1,
            "max_length": 32,
        }
    )
    crd: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "min_length": 1,
            "max_length": 256,
        }
    )
    stc: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "pattern": r"[0-9]{1,4}",
        }
    )
    stt: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "min_length": 1,
            "max_length": 32,
        }
    )
    pri: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "pattern": r"[0-9]{1}",
        }
    )
    lco: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "pattern": r"[0-9]{1,3}",
        }
    )
    lva: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "min_length": 1,
            "max_length": 2,
        }
    )
    lge: Optional["Mrq.Lge"] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    lte: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "min_length": 1,
            "max_length": 32,
        }
    )
    ico: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "pattern": r"[0-9]{1,3}",
        }
    )
    ite: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "min_length": 1,
            "max_length": 128,
        }
    )
    ame: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "pattern": r"[01]?",
        }
    )

    @dataclass
    class Lge:
        content: List[object] = field(
            default_factory=list,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
                "mixed": True,
            }
        )
        geo: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "pattern": r"[0-9\.,]{1,23}",
            }
        )
        tim: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "pattern": r"[0-9\-:\+T]{22}",
            }
        )
        gga: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "min_length": 0,
                "max_length": 81,
            }
        )


@dataclass
class Mrs:
    class Meta:
        name = "mrs"

    ref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
            "pattern": r"[0-9a-zA-Z]{1,16}",
        }
    )
    snu: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
            "pattern": r"[0-9]{1,5}",
        }
    )
    ste: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "min_length": 1,
            "max_length": 128,
        }
    )
    cve: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "pattern": r"[0-9]{2}\.[0-9]{2}",
        }
    )
    mre: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "pattern": r"[0-9]{2}",
        }
    )
    cre: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "pattern": r"[0-9]{2}",
        }
    )
    tnu: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "min_length": 1,
            "max_length": 256,
        }
    )
    hbi: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "pattern": r"[0-4]{1}",
        }
    )

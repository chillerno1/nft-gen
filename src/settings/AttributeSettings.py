from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, List, Dict, Any

from model.Attribute import Attribute


@dataclass
class AttributeSettings:
    attribute: Attribute
    weight: float
    position: Tuple[int, int]
    anchor_point: Tuple[float, float]
    slots:  List[Slot]


@dataclass
class Slot:
    feature: str
    position: Tuple[int, int]
    attributes_section: Dict[str, Any]

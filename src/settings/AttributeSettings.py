from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict, Any

from model.Attribute import Attribute


@dataclass
class AttributeSettings:
    attribute: Attribute
    weight: Optional[float] = None
    offset: Optional[Tuple[int, int]] = None
    anchor_point: Optional[Tuple[float, float]] = None
    slots:  Optional[List[Slot]] = None


@dataclass
class Slot:
    feature: str
    position: Tuple[int, int]
    attributes_section: Dict[str, Any]

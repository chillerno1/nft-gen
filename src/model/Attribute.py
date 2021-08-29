from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict

from model.Feature import Feature
from model.Position import Position


@dataclass
class Attribute:
    name: str
    feature: Feature
    weight: Optional[float] = None
    offset: Optional[Tuple[float, float]] = None
    anchor_point: Optional[Tuple[float, float]] = None
    slots:  Optional[List[Slot]] = None

    def __str__(self):  # TODO: remove
        string = "    " + str(self.name)
        string += "\n        feature: " + str(self.feature)
        string += "\n        weight: " + str(self.weight)
        string += "\n        offset: " + str(self.offset)
        string += "\n        anchor_point: " + str(self.anchor_point)
        string += "\n        slots:"
        if self.slots is not None:
            for s in self.slots:
                string += "\n            -" + str(s)
        return string


@dataclass
class Slot:
    feature: Feature
    attributes: Dict[str, Attribute]


class Species(Attribute):  # TODO: remove
    def __init__(self, name: str, eyes_pos: Position, mouth_pos: Position):
        super().__init__(name, Feature.BODY)

        self.eyes_position = eyes_pos
        self.mouth_position = mouth_pos

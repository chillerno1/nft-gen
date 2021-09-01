from dataclasses import dataclass
from typing import Tuple

from model.Attribute import Attribute


@dataclass
class ImageData:
    attribute: Attribute
    position: Tuple[float, float]
    anchor_point: Tuple[float, float]

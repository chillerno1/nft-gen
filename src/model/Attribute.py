from dataclasses import dataclass

from model.Feature import Feature


@dataclass
class Attribute:
    name: str
    feature: Feature

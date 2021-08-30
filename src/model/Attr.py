from dataclasses import dataclass

from model.Feature import Feature


@dataclass
class Attr:
    name: str
    feature: Feature

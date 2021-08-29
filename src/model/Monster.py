from dataclasses import dataclass

from model.Attribute import Attribute, Species


@dataclass
class Monster:
    species: Species
    attributes: [Attribute]

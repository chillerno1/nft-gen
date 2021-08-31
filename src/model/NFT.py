from dataclasses import dataclass
from typing import Dict

from PIL.Image import Image

from model.Attribute import Attribute


@dataclass
class NFT:
    image: Image
    attributes: Dict[str, str]

    def add_attribute(self, attribute: Attribute):
        feature = attribute.feature
        if feature in self.attributes:
            raise RuntimeError(f"An attribute was already picked for the feature: {feature}")
        self.attributes[feature] = attribute.name

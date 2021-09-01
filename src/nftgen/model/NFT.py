from dataclasses import dataclass
from typing import Dict, List

from PIL.Image import Image

from nftgen.image.image_assets import compose, get_image
from nftgen.model.ImageData import ImageData
from nftgen.model.Position import Position
from nftgen.settings import config


@dataclass
class NFT:
    name: str
    image_data: List[ImageData]

    def get_properties(self) -> Dict[str, str]:
        d = {}
        for data in self.image_data:
            d[data.attribute.feature] = data.attribute.name
        return d

    def create_image(self, background: Image) -> Image:
        image = background
        used_features = []

        for data in self.image_data:
            if data.attribute.feature in used_features:
                raise RuntimeError(f"Duplicate feature: {data.attribute.feature}")
            used_features.append(data.attribute.feature)

            new_image = get_image(data.attribute, config.assets_scale)
            position = Position(data.position, data.anchor_point, (new_image.width, new_image.height))
            compose(image, new_image, position)

        return image

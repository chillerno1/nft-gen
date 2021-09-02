from dataclasses import dataclass
from typing import Dict, List, Tuple

from PIL.Image import Image
from nftgen.image.ColorMatch import ColorMatch

from nftgen.image.image_colors import colorize, rgb_to_hue

from nftgen.image.image_assets import compose, get_image
from nftgen.model.ImageData import ImageData
from nftgen.model.Position import Position
from nftgen.settings import config


@dataclass
class NFT:
    name: str
    image_data: List[ImageData]
    color: Tuple[str, str]

    def get_properties(self) -> Dict[str, str]:
        d = {}
        for data in self.image_data:
            d[data.attribute.feature] = data.attribute.name
        d["Color"] = self.color[0]

        sorted_dict = {}
        for i in sorted(d.items(), key=lambda x: x[0].lower()):
            sorted_dict[i[0]] = i[1]

        return sorted_dict

    def create_image(self, background: Image) -> Image:
        image = background
        used_features = []

        for data in self.image_data:
            if data.attribute.feature in used_features:
                raise RuntimeError(f"Duplicate feature: {data.attribute.feature}")
            used_features.append(data.attribute.feature)

            new_image = get_image(data.attribute)
            new_image = colorize(new_image, rgb_to_hue(self.color[1]), ColorMatch(config.color_placeholder_hue, 1))

            position = Position(data.position, data.anchor_point, (new_image.width, new_image.height))
            compose(image, new_image, position)

        return image

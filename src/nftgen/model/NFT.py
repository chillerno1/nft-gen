from dataclasses import dataclass
from typing import Dict, List

from PIL.Image import Image
from nftgen.settings import config

from nftgen.image.image_assets import compose, get_image_components
from nftgen.model import Attribute
from nftgen.model.ImageData import ImageData
from nftgen.model.Position import Position
from nftgen.settings.ColorTheme import ColorTheme


@dataclass
class NFT:
    name: str
    image_data: List[ImageData]
    color: ColorTheme

    def get_properties(self) -> Dict[str, str]:
        d = {}
        for data in self.image_data:
            d[data.attribute.feature] = data.attribute.name_without_color()
        d["Color"] = self.color.name

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

            new_image = self.compose_components(data.attribute)

            position = Position(data.position, data.anchor_point, (new_image.width, new_image.height))
            compose(image, new_image, position)

        return image

    def compose_components(self, attribute: Attribute) -> Image:
        components = get_image_components(attribute)
        base = None
        for component in components:
            name = component[0]
            image = component[1]

            if config.primary_color_sign in name:
                image = self.color.primary.apply(image)
            elif config.accent_color_sign in name:
                image = self.color.accent.apply(image)

            if base is None:
                base = image
            else:
                compose(base, image)
        return base

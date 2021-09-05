import os
import warnings
from typing import Optional, List, Tuple

from PIL import Image as img
from PIL.Image import Image

from nftgen.model.Attribute import Attribute
from nftgen.model.Position import Position
from nftgen.settings import config


def create_background() -> Image:
    return img.new(mode="RGBA", size=(config.size, config.size), color=config.background_color)


def _get_asset(asset_name: str, scale: Optional[float] = None) -> Optional[Image]:
    path = f"{config.assets_dir}/{asset_name}.png"
    if not os.path.exists(path):
        warnings.warn(f"Could not find asset: {path}")
        return None
    image = img.open(path)
    if scale is not None and scale != 1:
        image = image.resize((round(image.width * scale), round(image.height * scale)))
    return image


def get_shadow() -> Optional[Image]:
    return _get_asset("shadow", config.assets_scale)


def get_image(attribute: Attribute) -> Image:
    return _get_asset(f"{attribute.feature}/{attribute.name}", config.assets_scale)


def get_image_components(attribute: Attribute) -> List[Tuple[str, Image]]:
    path = f"{config.assets_dir}/{attribute.feature}/{attribute.name}"

    if not os.path.isdir(path):
        return [(attribute.name, get_image(attribute))]

    result = []
    for file in os.listdir(path):
        name_split = os.path.splitext(file)
        if name_split[1] == ".png":
            result.append((
                name_split[0],
                _get_asset(f"{attribute.feature}/{attribute.name}/{name_split[0]}", config.assets_scale),
            ))

    return result


def compose(background: Image, image: Image, position: Position = Position((0, 0))):
    background.alpha_composite(image, position.point)

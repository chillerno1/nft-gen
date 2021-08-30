from typing import Tuple

from PIL import Image

import config
from model.AttributeSettings import AttributeSettings
from model.Position import Position


def create_background() -> Image:
    return Image.new(mode="RGB", size=(config.size, config.size), color=config.background_color)


def get_image(attribute_settings: AttributeSettings) -> Image:
    return Image.open(
        f"{config.images_dir}/"
        f"{attribute_settings.attribute.feature}/"
        f"{attribute_settings.attribute.name}"
        f".png"
    )


def compose(background: Image, image: Image, position: Position):
    background.paste(image, _get_image_position(background, image, position), image)


def _get_image_position(
        background_image: Image,
        image: Image,
        position: Position
) -> Tuple[int, int]:
    x = int(round(background_image.width * position.x - image.width * position.anchor_point[0]))
    y = int(round(background_image.height * (1 - position.y) - image.height * (1 - position.anchor_point[1])))
    return x, y

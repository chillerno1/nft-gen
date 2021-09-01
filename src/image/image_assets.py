from PIL import Image

from model.Attribute import Attribute
from model.Position import Position
from settings import config


def create_background() -> Image:
    return Image.new(mode="RGBA", size=(config.size, config.size), color=config.background_color)


def get_shadow() -> Image:
    return Image.open(
        f"{config.images_dir}/"
        f"shadow"
        f".png"
    )


def get_image(attribute: Attribute) -> Image:
    return Image.open(
        f"{config.images_dir}/"
        f"{attribute.feature}/"
        f"{attribute.name}"
        f".png"
    )


def compose(background: Image, image: Image, position: Position):
    background.paste(image, position.point, image)


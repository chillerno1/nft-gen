from PIL import Image

from settings import config
from settings.AttributeSettings import AttributeSettings
from model.Position import Position


def create_background() -> Image:
    return Image.new(mode="RGBA", size=(config.size, config.size), color=config.background_color)


def get_image(attribute_settings: AttributeSettings) -> Image:
    return Image.open(
        f"{config.images_dir}/"
        f"{attribute_settings.attribute.feature}/"
        f"{attribute_settings.attribute.name}"
        f".png"
    )


def compose(background: Image, image: Image, position: Position):
    background.paste(image, position.point, image)


import numpy as np
from PIL import Image

from settings.parse_attributes import get_base_slots
from randomizer import generate_random_attr
from utils.image_utils import create_background, get_image, compose
from settings.AttributeSettings import Slot
from model.Position import Position


def generate() -> Image:
    image = create_background()

    base_slots = get_base_slots()

    for base_slot in base_slots:
        fill(image, base_slot, Position((image.width / 2, image.height / 2)))

    return image


def fill(image: Image, slot: Slot, base_pos: Position):
    attribute_settings = generate_random_attr(slot)
    if attribute_settings.attribute.name == "none":
        return

    new_image = get_image(attribute_settings)
    pos = Position(
        tuple(
            np.add(
                base_pos.base_point,
                attribute_settings.offset,
            )
        ),
        attribute_settings.anchor_point,
        (new_image.width, new_image.height),
    )

    for slot in attribute_settings.slots:
        if slot.behind:
            fill(image, slot, pos)

    compose(image, new_image, pos)

    for slot in attribute_settings.slots:
        if not slot.behind:
            fill(image, slot, pos)

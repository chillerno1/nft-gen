import operator
from typing import Tuple

from PIL import Image

from attributes_handler import get_base_slots
from randomizer import generate_random_attr
from utils.image_utils import create_background, get_image, compose
from model.AttributeSettings import Slot
from model.Position import Position


def generate() -> Image:
    image = create_background()

    base_slots = get_base_slots()

    for base_slot in base_slots:
        fill(image, base_slot, (0.5, 0.5))

    return image


def fill(image: Image, slot: Slot, base_pos: Tuple[float, float]):
    attribute_settings = generate_random_attr(slot)
    pos = Position(tuple(map(operator.add, base_pos, attribute_settings.offset)), attribute_settings.anchor_point)

    for slot in attribute_settings.slots:
        if slot.behind:
            fill(image, slot, pos.point)

    if attribute_settings.attribute.name != "none":
        compose(image, get_image(attribute_settings), pos)

    for slot in attribute_settings.slots:
        if not slot.behind:
            fill(image, slot, pos.point)

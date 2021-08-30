import operator
from typing import Tuple

from PIL import Image

from attributes_handler import get_base_slots
from randomizer import generate_random_attr
from utils.image_utils import create_background, get_image, compose
from model.Attribute import Slot
from model.Position import Position


def generate() -> Image:
    image = create_background()

    base_slots = get_base_slots()

    for base_slot in base_slots:
        fill(image, base_slot, (0.5, 0.5))

    return image


def fill(image: Image, slot: Slot, base_pos: Tuple[float, float]):
    attr = generate_random_attr(slot)
    pos = Position(tuple(map(operator.add, base_pos, attr.offset)), attr.anchor_point)

    for slot in attr.slots:
        if slot.behind:
            fill(image, slot, pos.point)

    if attr.name != "none":
        compose(image, get_image(attr), pos)

    for slot in attr.slots:
        if not slot.behind:
            fill(image, slot, pos.point)

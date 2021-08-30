import operator
from typing import List, Tuple

from PIL import Image

from attributes_handler import get_base_features, get_base_slots
from randomizer import generate_random_attr
from utils.color_utils import colorize
from utils.image_utils import create_background, get_image, compose
from model.Feature import Feature
from model.Attribute import Attribute, Species, Slot
from model.Monster import Monster
from model.Position import Position


def generate(species: int, eyes: int, mouth: int) -> Image:
    image = create_background()

    species_attr = species_types[species]
    eyes_attr = eyes_types[eyes]
    mouth_attr = mouth_types[mouth]

    compose(image, colorize(get_image(species_attr), 270), body_position)
    compose(image, get_image(eyes_attr), species_attr.eyes_position)
    compose(image, get_image(mouth_attr), species_attr.mouth_position)

    return image


def generate2() -> Image:
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


def get_image_of_monster(monster: Monster) -> Image:
    image = create_background()

    for attr in monster.attributes:
        compose(image, get_image(attr), monster.species.eyes_position)  # TODO: position depend on feature

    return image


body_position = Position((0.50, 0.14), anchor_point=(0.50, 0))

species_types = [
    Species(name="Base", eyes_pos=Position((0.50, 0.62)), mouth_pos=Position((0.50, 0.40))),
]
eyes_types = [
        Attribute(name="One", feature=Feature.EYES),
        Attribute(name="Two", feature=Feature.EYES),
        Attribute(name="Three", feature=Feature.EYES),
    ]
mouth_types = [
        Attribute(name="Bunny", feature=Feature.MOUTH),
        Attribute(name="Happy", feature=Feature.MOUTH),
        Attribute(name="Open Big", feature=Feature.MOUTH),
    ]

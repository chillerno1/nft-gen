import numpy as np

from model.NFT import NFT
from settings.parse_attributes import get_base_slots
from randomizer import generate_random_attr
from utils.image_utils import create_background, get_image, compose, get_shadow
from settings.AttributeSettings import Slot
from model.Position import Position


def generate() -> NFT:
    background = create_background()
    shadow = get_shadow()
    compose(background, shadow, Position((background.width / 2, 875), (0.5, 0.5), (shadow.width, shadow.height)))
    nft = NFT(background, {})

    base_slots = get_base_slots()

    for base_slot in base_slots:
        fill(nft, base_slot, Position((background.width / 2, background.height / 2)))

    return nft


def fill(nft: NFT, slot: Slot, base_pos: Position):
    attribute_settings = generate_random_attr(slot)

    nft.add_attribute(attribute_settings.attribute)

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
            fill(nft, slot, pos)

    compose(nft.image, new_image, pos)

    for slot in attribute_settings.slots:
        if not slot.behind:
            fill(nft, slot, pos)

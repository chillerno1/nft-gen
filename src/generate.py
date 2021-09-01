from typing import List, Tuple

import numpy as np
from PIL.Image import Image

from model.ImageData import ImageData
from model.NFT import NFT
from settings import config
from settings.parse_attributes import get_base_slots
from randomizer import generate_random_attr
from image.image_assets import create_background, compose, get_shadow
from settings.AttributeSettings import Slot
from model.Position import Position


def create_image(nft: NFT) -> Image:
    size = config.size
    background = create_background()
    shadow = get_shadow()
    compose(background, shadow, Position(np.add((size / 2, size / 2), config.shadow_position), (0.5, 0.5), (shadow.width, shadow.height)))

    return nft.create_image(background)


def generate() -> NFT:
    size = config.size
    width = size
    height = size

    image_data = []
    for base_slot in get_base_slots():
        for data in generate_for_slot(base_slot, (width / 2, height / 2))[0]:
            image_data.append(data)

    return NFT(image_data)


def generate_for_slot(base_slot: Slot, base_pos: Tuple[int, int]) -> Tuple[List[ImageData], bool]:
    settings = generate_random_attr(base_slot)

    if settings.attribute.name == "none":
        return [], False

    pos = tuple(
        np.add(
            np.add(
                base_pos,
                base_slot.position,
            ),
            settings.position,
        )
    )

    image_data = ImageData(
        attribute=settings.attribute,
        position=pos,
        anchor_point=settings.anchor_point,
    )

    background = []
    foreground = []

    for slot in settings.slots:
        datas_behind = generate_for_slot(slot, pos)
        datas = datas_behind[0]
        behind = datas_behind[1]

        if behind:
            background.extend(datas)
        else:
            foreground.extend(datas)

    datas = []

    datas.extend(background)
    datas.append(image_data)
    datas.extend(foreground)

    return datas, settings.behind

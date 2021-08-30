import random
from typing import Dict, List

from attributes_handler import get_all_attribute_names, get_attribute_from_settings_with_defaults
from model.Attribute import Attribute, Slot


def fill_slots(slots: List[Slot]):
    for slot in slots:
        attr = generate_random_attr(slot)
        fill_slots(attr.slots)


def generate_random_attr(slot: Slot) -> Attribute:
    attribute_names = get_all_attribute_names(slot.feature)
    attributes_by_name: Dict[str, Attribute] = {}

    total_weight = 0
    weights_by_name: Dict[str, float] = {}

    for name in attribute_names:
        attribute = get_attribute_from_settings_with_defaults(slot.attributes, name, slot.feature)
        attributes_by_name[name] = attribute

        total_weight += attribute.weight
        weights_by_name[name] = total_weight

    r = random.uniform(0, total_weight)

    chosen_name = next(key for key, value in weights_by_name.items() if r < value)

    return attributes_by_name[chosen_name]

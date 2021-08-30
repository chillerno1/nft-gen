import random
from typing import Dict

from model.Attribute import Attribute
from model.AttributeSettings import AttributeSettings, Slot
from parse_attributes import get_all_attribute_names, get_attribute_from_settings_with_defaults


def generate_random_attr(slot: Slot) -> AttributeSettings:
    attribute_names = get_all_attribute_names(slot.feature)
    attributes_by_name: Dict[str, AttributeSettings] = {}

    total_weight = 0
    weights_by_name: Dict[str, float] = {}

    for name in attribute_names:
        attribute = get_attribute_from_settings_with_defaults(slot.attributes, Attribute(name=name, feature=slot.feature))
        attributes_by_name[name] = attribute

        total_weight += attribute.weight
        weights_by_name[name] = total_weight

    r = random.uniform(0, total_weight)

    chosen_name = next(key for key, value in weights_by_name.items() if r < value)

    return attributes_by_name[chosen_name]

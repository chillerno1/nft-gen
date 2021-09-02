import random
from typing import Dict

from nftgen.settings.AttributeSettings import AttributeSettings, Slot
from nftgen.settings.parse_attributes import get_settings_from_slot, get_all_attribute_names


def generate_random_attr(slot: Slot) -> AttributeSettings:
    attribute_names = get_all_attribute_names(slot.feature)
    if len(attribute_names) == 0:
        return get_settings_from_slot("none", slot)

    attributes_by_name: Dict[str, AttributeSettings] = {}

    total_weight = 0
    weights_by_name: Dict[str, float] = {}

    for name in attribute_names:
        attribute = get_settings_from_slot(name, slot)
        attributes_by_name[name] = attribute

        total_weight += attribute.weight
        weights_by_name[name] = total_weight

    r = random.uniform(0, total_weight)

    chosen_name = next(key for key, value in weights_by_name.items() if r < value)

    return attributes_by_name[chosen_name]

import os
from typing import List, Set, Dict, Hashable, Any

import config
from model.Attribute import Attribute
from model.AttributeSettings import AttributeSettings, Slot
from model.Feature import Feature
from parse_attributes import _strip_extension, _get_base_attribute, data_map, default_weight, \
    default_offset, default_anchor_point, _parse_slots, _get_attribute_from_settings
from utils.none import not_none


def get_base_slots() -> List[Slot]:
    return _parse_slots(data_map.get("slots"))


def get_attribute(attribute: Attribute) -> AttributeSettings:
    attribute = not_none(_get_base_attribute(attribute), AttributeSettings(attribute=attribute))

    attribute.weight = not_none(attribute.weight, default_weight)
    attribute.offset = not_none(attribute.offset, default_offset)
    attribute.anchor_point = not_none(attribute.anchor_point, default_anchor_point)
    attribute.slots = not_none(attribute.slots, [])

    return attribute


def populate_defaults(attribute_settings: AttributeSettings) -> AttributeSettings:
    default = get_attribute(attribute_settings.attribute)

    attribute_settings.weight = not_none(attribute_settings.weight, default.weight)
    attribute_settings.offset = not_none(attribute_settings.offset, default.offset)
    attribute_settings.anchor_point = not_none(attribute_settings.anchor_point, default.anchor_point)
    attribute_settings.slots = not_none(attribute_settings.slots, default.slots)

    return attribute_settings


def get_attribute_from_settings_with_defaults(
        attribute_settings: Dict[Hashable, Any],
        attribute: Attribute,
) -> AttributeSettings:
    return populate_defaults(_get_attribute_from_settings(attribute_settings, attribute))


def get_all_attribute_names(feature: Feature) -> Set[str]:
    file_names = os.listdir(f"{config.images_dir}/{feature.name.lower()}")
    return set(map(_strip_extension, file_names))

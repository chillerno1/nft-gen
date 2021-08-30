import os
from typing import List, Set

import config
from model.Attribute import Attribute, Slot
from model.Feature import Feature
from parse_attributes import _string_to_feature, _strip_extension, _get_base_attribute, data_map, default_weight, \
    default_offset, default_anchor_point, _parse_slots, _get_attribute_from_settings


def get_base_features() -> List[Feature]:
    return list(map(_string_to_feature, data_map.get("features")))


def get_base_slots() -> List[Slot]:
    return _parse_slots(data_map.get("slots"))


def get_attribute(
        feature: Feature,
        name: str,
) -> Attribute:
    attribute = _get_base_attribute(feature, name) or Attribute(name=name, feature=feature)

    attribute.weight = attribute.weight or default_weight
    attribute.offset = attribute.offset or default_offset
    attribute.anchor_point = attribute.anchor_point or default_anchor_point
    attribute.slots = attribute.slots or []

    return attribute


def populate_defaults(attribute: Attribute) -> Attribute:
    default = get_attribute(attribute.feature, attribute.name)

    attribute.weight = attribute.weight or default.weight
    attribute.offset = attribute.offset or default.offset
    attribute.anchor_point = attribute.anchor_point or default.anchor_point
    attribute.slots = attribute.slots or default.slots

    return attribute


def get_attribute_from_settings_with_defaults(attribute_settings, name: str, feature: Feature) -> Attribute:
    return populate_defaults(_get_attribute_from_settings(attribute_settings, name, feature))


def get_all_attribute_names(feature: Feature) -> Set[str]:
    file_names = os.listdir(f"{config.images_dir}/{feature.name.lower()}")
    return set(map(_strip_extension, file_names))

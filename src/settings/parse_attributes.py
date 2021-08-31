from __future__ import annotations

import os
from typing import Dict, List, Any, Optional, Set
import yaml

from settings import config
from model.Attribute import Attribute
from settings.AttributeSettings import AttributeSettings, Slot
from utils.none import not_none

_attributes_path = "attributes.yaml"

with open(_attributes_path) as file:
    data_map = yaml.safe_load(file)

_defaults = data_map.get("default")
_default_weight = _defaults.get("weight")
_default_offset = eval(_defaults.get("offset"))
_default_anchor_point = eval(_defaults.get("anchor_point"))


def get_base_slots() -> List[Slot]:
    return _parse_slots(data_map.get("slots"))


def get_attribute_from_settings_with_defaults(
        attributes_section: Dict[str, Any],
        attribute: Attribute,
) -> AttributeSettings:
    return _populate_defaults(_get_attribute_from_settings(attributes_section, attribute))


def get_all_attribute_names(feature: str) -> Set[str]:
    file_names = os.listdir(f"{config.images_dir}/{feature}")
    return set(map(_strip_extension, file_names))


def _get_attribute(attribute: Attribute) -> AttributeSettings:
    attribute = not_none(_get_base_attribute(attribute), AttributeSettings(attribute=attribute))

    attribute.weight = not_none(attribute.weight, _default_weight)
    attribute.offset = not_none(attribute.offset, _default_offset)
    attribute.anchor_point = not_none(attribute.anchor_point, _default_anchor_point)
    attribute.slots = not_none(attribute.slots, [])

    return attribute


def _populate_defaults(attribute_settings: AttributeSettings) -> AttributeSettings:
    default = _get_attribute(attribute_settings.attribute)

    attribute_settings.weight = not_none(attribute_settings.weight, default.weight)
    attribute_settings.offset = not_none(attribute_settings.offset, default.offset)
    attribute_settings.anchor_point = not_none(attribute_settings.anchor_point, default.anchor_point)
    attribute_settings.slots = not_none(attribute_settings.slots, default.slots)

    return attribute_settings


def _get_base_attribute(attribute: Attribute) -> AttributeSettings:
    feature_settings = data_map.get("feature_settings")
    attributes_section = feature_settings.get(attribute.feature, {})
    attribute_settings = _get_attribute_from_settings(attributes_section, attribute)

    return attribute_settings


def _get_base_attribute_settings(feature: str):
    feature_settings = data_map.get("feature_settings")
    attributes_section = feature_settings.get(feature)

    return attributes_section


def _get_attribute_from_settings(attributes_section: Dict[str, Any], attribute: Attribute) -> AttributeSettings:
    default_values = attributes_section.get("default", {})
    values = attributes_section.get(attribute.name, {})

    return AttributeSettings(
        attribute=attribute,
        weight=_get_or("weight", values, default_values),
        offset=_get_or("offset", values, default_values),
        anchor_point=_get_or("anchor_point", values, default_values),
        slots=_parse_slots(values.get("slots", default_values.get("slots"))),
    )


def _parse_slots(values) -> Optional[List[Slot]]:
    if values is None:
        return None
    return list(map(_parse_slot, values))


def _parse_slot(values) -> Slot:
    feature = values.get("feature")
    behind = bool(values.get("behind", False))
    attributes_section = values.get("attributes", _get_base_attribute_settings(feature))

    return Slot(
        feature=feature,
        behind=behind,
        attributes_section=attributes_section,
    )


def _get_or(key: str, values: Dict[str, Any], default_values: Dict[str, Any]):
    it = values.get(key, None)

    if it is None:
        it = default_values.get(key, None)

    return eval(str(it))


def _strip_extension(file_name) -> str:
    return os.path.splitext(file_name)[0]

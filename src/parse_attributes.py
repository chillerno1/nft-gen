from __future__ import annotations

import os
from typing import Dict, List, Hashable, Any, Optional
import yaml

from model.Attribute import Attribute
from model.AttributeSettings import AttributeSettings, Slot


_attributes_path = "attributes.yaml"

with open(_attributes_path) as file:
    data_map = yaml.safe_load(file)

_defaults = data_map.get("default")
default_weight = _defaults.get("weight")
default_offset = eval(_defaults.get("offset"))
default_anchor_point = eval(_defaults.get("anchor_point"))


def _get_base_attribute(attribute: Attribute) -> AttributeSettings:
    feature_settings = data_map.get("feature_settings")
    attributes_section = feature_settings.get(attribute.feature)
    attribute_settings = _get_attribute_from_settings(attributes_section, attribute)

    return attribute_settings


def _get_base_attribute_settings(feature: str):
    feature_settings = data_map.get("feature_settings")
    attributes_section = feature_settings.get(feature)

    return attributes_section


def _get_attribute_from_settings(attribute_settings: Dict[Hashable, Any], attribute: Attribute) -> AttributeSettings:
    default_values = attribute_settings.get("default", {})
    values = attribute_settings.get(attribute.name, {})

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
        attributes=attributes_section,
    )


def _get_or(key: str, values: Dict[Hashable, Any], default_values: Dict[Hashable, Any]):
    it = values.get(key, None)

    if it is None:
        it = default_values.get(key, None)

    return eval(str(it))


def _strip_extension(file_name) -> str:
    return os.path.splitext(file_name)[0]

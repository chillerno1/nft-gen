from __future__ import annotations

import os
from typing import Dict, List, Hashable, Any, Optional
import yaml

from model.Attribute import Attribute, Slot
from model.Feature import Feature


_attributes_path = "attributes.yaml"

with open(_attributes_path) as file:
    data_map = yaml.safe_load(file)

_defaults = data_map.get("default")
default_weight = _defaults.get("weight")
default_offset = _defaults.get("offset")
default_anchor_point = _defaults.get("anchor_point")


def _get_attribute(
        feature: Feature,
        name: str,
) -> Attribute:
    features = data_map.get("feature_settings")
    attributes_section = features.get(feature.name)
    attributes = _parse_attributes_section(feature.name, attributes_section)

    attribute = next((a for a in attributes if a.name == name), None)

    return attribute


def _get_attributes() -> Dict[Feature, List[Attribute]]:
    attributes_by_feature = _parse_attributes(data_map.get("feature_settings"))

    return attributes_by_feature


def _parse_attributes(section) -> Dict[Feature, List[Attribute]]:
    attributes_by_feature: Dict[Feature, List[Attribute]] = {}

    for feature in section.keys():
        attributes = _parse_attributes_section(feature, section.get(feature))
        attributes_by_feature[feature] = attributes

    return attributes_by_feature


def _parse_attributes_section(feature: str, section) -> List[Attribute]:
    attributes: List[Attribute] = []

    default_values = section.get("default")

    for name in section.keys():
        if name != "default":
            attribute_values = section.get(name)
            attribute_values["name"] = name
            attribute_values["feature"] = feature

            attributes.append(_parse_attribute(attribute_values, default_values))

    return attributes


def _parse_attribute(values, default_values) -> Attribute:
    return Attribute(
        name=str(values.get("name")),
        feature=Feature[values.get("feature")],
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
    attributes_section = values.get("attributes", {})
    attributes = {
        a.name: a for a in _parse_attributes_section(feature, attributes_section)
    }

    return Slot(
        feature=feature,
        attributes=attributes,
    )


def _get_or(key: str, values: Dict[Hashable, Any], default_values: Dict[Hashable, Any]):
    it = values.get(key, None)

    if it is None:
        it = default_values.get(key, None)

    return eval(str(it))


def _string_to_feature(string: str):
    return Feature[string]


def _strip_extension(file_name) -> str:
    return os.path.splitext(file_name)[0]

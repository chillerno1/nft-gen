import os
from typing import List, Set

import config
from model.Attribute import Attribute
from model.Feature import Feature
from parse_attributes import _get_attributes, _string_to_feature, _strip_extension, \
    _get_attribute, data_map, default_weight, default_offset, default_anchor_point


def test():  # TODO: remove
    for s in get_all_attribute_names(Feature.EYES):
        print(s)

    for al in _get_attributes().values():
        for a in al:
            print(populate_defaults(a))


def get_base_features() -> List[Feature]:
    return list(map(_string_to_feature, data_map.get("features")))


def get_attribute(
        feature: Feature,
        name: str,
) -> Attribute:
    return _get_attribute(feature, name)


def populate_defaults(attribute: Attribute) -> Attribute:
    default = get_attribute(attribute.feature, attribute.name)

    attribute.weight = attribute.weight or default.weight or default_weight
    attribute.offset = attribute.offset or default.offset or default_offset
    attribute.anchor_point = attribute.anchor_point or default.anchor_point or default_anchor_point
    attribute.slots = attribute.slots or default.slots or []

    return attribute


def get_all_attribute_names(feature: Feature) -> Set[str]:
    file_names = os.listdir(f"{config.images_dir}/{feature.name.lower()}")
    return set(map(_strip_extension, file_names))

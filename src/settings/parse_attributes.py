import os
from typing import Dict, Any, List, Optional, Set

import yaml

from model.Attribute import Attribute
from settings import config
from settings.AttributeSettings import Slot, AttributeSettings
from utils.none import get_value_safe, not_none

_attributes_path = "attributes.yaml"

with open(_attributes_path) as file:
    data_map = yaml.safe_load(file)

_slots_section = get_value_safe(data_map, "base-slots", [])
_defaults_section = get_value_safe(data_map, "default", {})
_attribute_settings_section = get_value_safe(data_map, "attribute-settings", {})

_default_name = "default"
_default_weight = float(str(_defaults_section.get("weight", 1)))
_default_position = eval(str(_defaults_section.get("position", (0, 0))))
_default_anchor_point = eval(str(_defaults_section.get("anchor_point", (0, 0))))
_default_behind = bool(str(_defaults_section.get("behind", False)))
_default_slots = []


def get_base_slots() -> List[Slot]:
    """Returns the base slots to start the generation from."""
    return _parse_slots(_slots_section)


def get_all_attribute_names(feature: str) -> Set[str]:
    file_names = os.listdir(f"{config.images_dir}/{feature}")
    return set(map(_strip_extension, file_names))


def get_settings_from_slot(name: str, slot: Slot) -> AttributeSettings:
    return _get_settings_from_section(Attribute(name=name, feature=slot.feature), slot.attributes_section)


def _get_settings_from_section(attribute: Attribute, attributes_section: Dict[str, Any]) -> AttributeSettings:
    """
    Returns the settings for the `attribute` given the `attributes_section`. Settings not found in the given section
    use the defaults instead.

    :param attribute: the attribute to get the base settings for
    :param attributes_section: the section to get the priority settings from
    :return: the attribute settings
    """
    settings = _get_base_attribute_settings(attribute)
    _populate(settings, get_value_safe(attributes_section, _default_name, {}))
    _populate(settings, get_value_safe(attributes_section, attribute.name, {}))

    return settings


def _get_base_attribute_settings(attribute: Attribute) -> AttributeSettings:
    """
    Returns the base settings for the `attribute`.

    :param attribute: the attribute to get the base settings for
    :return: the attribute settings
    """
    base_section = _get_base_attributes_section(attribute.feature)

    settings = _get_default_attribute_settings(attribute)
    _populate(settings, get_value_safe(base_section, _default_name, {}))
    _populate(settings, get_value_safe(base_section, attribute.name, {}))

    return settings


def _get_base_attributes_section(feature: str) -> Dict[str, Any]:
    """
    Returns the base section of attribute settings for the `feature`.

    :param feature: the feature to get the attribute settings for
    :return: a section of attribute settings
    """
    return get_value_safe(_attribute_settings_section, feature, {})


def _populate(settings: AttributeSettings, values: Dict[str, Any]) -> AttributeSettings:
    """
    Populates the `settings` with the `values` ignoring ones that are not present.

    :param settings: the settings to populate
    :param values: the values to populate the settings with
    :return: the settings
    """
    settings.weight = float(str(get_value_safe(values, "weight", settings.weight)))
    settings.position = eval(str(get_value_safe(values, "position", settings.position)))
    settings.anchor_point = eval(str(get_value_safe(values, "anchor_point", settings.anchor_point)))
    settings.behind = bool(str(get_value_safe(values, "behind", settings.behind)))
    if "slots" in values.keys():
        settings.slots = _parse_slots(not_none(values.get("slots"), {}))
    return settings


def _parse_slots(slots_section: Dict[str, Any]) -> Optional[List[Slot]]:
    return [_parse_slot(feature, not_none(slots_section.get(feature), {})) for feature in slots_section]


def _parse_slot(feature: str, values: Dict[str, Any]) -> Slot:
    position = not_none(eval(str(values.get("position"))), (0, 0))
    attributes_section = get_value_safe(values, "attributes", {})
    return Slot(feature, position, attributes_section)


def _get_default_attribute_settings(attribute: Attribute) -> AttributeSettings:
    """
    Returns a new `AttributeSettings` for the `attribute` populated with the global default values.

    :param attribute: the attribute to create the settings for
    :return: the created attribute settings
    """
    return AttributeSettings(
        attribute=attribute,
        weight=_default_weight,
        position=_default_position,
        anchor_point=_default_anchor_point,
        behind=_default_behind,
        slots=_default_slots,
    )


def _strip_extension(file_name) -> str:
    return os.path.splitext(file_name)[0]

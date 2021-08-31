from typing import TypeVar, Optional, Dict, Any

T = TypeVar("T")


def not_none(t: Optional[T], default: T):
    """
    Returns `t` if not None, else `default`.

    :param t: the value to return if not None
    :param default: the default value to return
    :return: t if not None, else default
    """
    return t if t is not None else default


def get_value_safe(section: Optional[Dict[str, Any]], key: str, default: Any = None) -> Any:
    if section is None:
        return default

    val = section.get(key)
    if val is not None:
        return val
    return default

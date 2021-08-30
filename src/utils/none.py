from typing import TypeVar, Optional

T = TypeVar("T")


def not_none(t: Optional[T], default: T):
    """
    Returns `t` if not None, else `default`.

    :param t: the value to return if not None
    :param default: the default value to return
    :return: t if not None, else default
    """
    return t if t is not None else default

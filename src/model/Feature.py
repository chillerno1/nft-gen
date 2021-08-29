from enum import Enum


class Feature(Enum):
    BODY = True
    COLOR = True
    ARMS = False
    EYES = True
    MOUTH = True

    def __init__(self, required: bool):
        self.required = required

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

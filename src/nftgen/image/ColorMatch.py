from dataclasses import dataclass


@dataclass
class ColorMatch:
    hue: float
    diff: float

    def is_match(self, hue: float) -> bool:
        diff = abs(hue % 360 - self.hue % 360)
        if diff > 180:
            diff = 360 - diff
        res = diff <= self.diff
        return res

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from PIL.Image import Image

from nftgen.image.image_colors import gradient, colorize


@dataclass
class ColorTheme:
    name: str
    weight: float = 1
    primary: ColorSettings = None
    accent: ColorSettings = None


@dataclass
class ColorSettings:
    type: str
    color: str | Tuple[str, str]

    def apply(self, image) -> Image:
        if self.type.upper() == "GRADIENT":
            return gradient(image, self.color[0], self.color[1])
        else:
            return colorize(image, self.color)

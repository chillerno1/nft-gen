from dataclasses import dataclass

from nftgen.settings import config


@dataclass
class Attribute:
    name: str
    feature: str

    def name_without_color(self):
        return self.name.strip(config.primary_color_sign).strip(config.accent_color_sign)

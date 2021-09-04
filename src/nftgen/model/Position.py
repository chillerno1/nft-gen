from typing import Tuple

from nftgen.settings import config


class Position:
    def __init__(
            self,
            base_point: Tuple[float, float],
            anchor_point: Tuple[float, float] = (0.5, 0.5),
            size: Tuple[int, int] = (0, 0),
    ):
        world_size = 1
        if config.position_mode == "PERCENT":
            world_size = config.size
        elif config.position_mode == "PIXELS":
            world_size = 1

        self.base_point = base_point
        self.anchor_point = anchor_point
        self.size = size
        self.x = int(self.base_point[0] * world_size - round(self.size[0] * self.anchor_point[0]))
        self.y = int(self.base_point[1] * world_size - round(self.size[1] * self.anchor_point[1]))
        self.point = (self.x, self.y)

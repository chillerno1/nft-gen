from typing import Tuple


class Position:
    def __init__(
            self,
            base_point: Tuple[int, int],
            anchor_point: Tuple[float, float] = (0.5, 0.5),
            size: Tuple[int, int] = (0, 0),
    ):
        self.base_point = base_point
        self.anchor_point = anchor_point
        self.size = size
        self.x = int(self.base_point[0] - round(self.size[0] * self.anchor_point[0]))
        self.y = int(self.base_point[1] - round(self.size[1] * self.anchor_point[1]))
        self.point = (self.x, self.y)

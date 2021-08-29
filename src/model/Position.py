from typing import Tuple


class Position:
    def __init__(self, point: Tuple[float, float], anchor_point: Tuple[float, float] = (0.5, 0.5)):
        self.point = point
        self.anchor_point = anchor_point
        self.x = point[0]
        self.y = point[1]

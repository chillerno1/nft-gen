from dataclasses import dataclass
from typing import Callable, List


@dataclass
class Command:
    name: str
    aliases: List[str]
    executor: Callable

    def execute(self, *args):
        self.executor(*args)

from abc import ABC, abstractmethod
from typing import Self

from ai_simulations.common import Context


class Screen(ABC):
    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    @abstractmethod
    def handle_event(self) -> Self: ...

    @abstractmethod
    def update(self) -> None: ...

    @abstractmethod
    def draw(self) -> None: ...

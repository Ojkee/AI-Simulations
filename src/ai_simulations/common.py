from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import pygame

Color_t = tuple[int, int, int]


class Colors(Color_t, Enum):
    BEIGE = (255, 248, 231)
    GREY = (51, 51, 51)
    LIGHT_GREY = (131, 131, 131)
    LIGHTER_GREY = (171, 171, 171)
    RED = (255, 100, 100)
    GREEN = (100, 255, 100)


@dataclass
class Context:
    width: int
    height: int
    _surface: pygame.Surface | None = None
    _font: pygame.font.FontType | None = None

    @property
    def surface(self) -> pygame.Surface:
        if self._surface is None:
            raise ValueError("surface not set")
        return self._surface

    @surface.setter
    def surface(self, value: pygame.Surface) -> None:
        self._surface = value

    @property
    def font(self) -> pygame.font.FontType:
        if self._font is None:
            raise ValueError("font not set")
        return self._font

    @font.setter
    def font(self, value: pygame.font.FontType) -> None:
        self._font = value

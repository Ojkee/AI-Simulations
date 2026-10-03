from typing import Protocol, runtime_checkable

import pygame

from ai_simulations.common import Colors, Context


@runtime_checkable
class Intable(Protocol):
    def __int__(self) -> int: ...


class Button:
    def __init__(
        self,
        x: Intable,
        y: Intable,
        w: Intable,
        h: Intable,
        text: str,
    ) -> None:
        self._rect = pygame.Rect(int(x), int(y), int(w), int(h))
        self._text = text

    def draw(self, ctx: Context) -> None:
        color = Colors.LIGHTER_GREY if self.mouse_in_area() else Colors.LIGHT_GREY
        pygame.draw.rect(ctx.surface, color, self._rect, 2, 3)
        text = ctx.font.render(self._text, True, Colors.BEIGE)
        rect = text.get_rect()
        ctx.surface.blit(
            text,
            (
                self._rect.x + (self._rect.w - rect.w) // 2,
                self._rect.y + (self._rect.y + rect.h) // 2,
            ),
        )

    def mouse_in_area(self) -> bool:
        x, y = pygame.mouse.get_pos()
        in_x = self._rect.x <= x <= self._rect.x + self._rect.w
        in_y = self._rect.y <= y <= self._rect.y + self._rect.h
        return in_x and in_y

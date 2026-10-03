from typing import Self

import pygame

from ai_simulations.common import Colors, Context
from ai_simulations.screens.menu import Menu


class Window:
    def __init__(self, width: int, height: int) -> None:
        self.ctx = Context(width, height)
        self._running: bool = True

        self._current_screen = Menu(self.ctx)

    def __enter__(self) -> Self:
        pygame.init()
        pygame.font.init()
        self.ctx.surface = pygame.display.set_mode((self.ctx.width, self.ctx.height))
        self.ctx.font = pygame.font.SysFont(pygame.font.get_default_font(), 24)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        _ = exc_type, exc_value, traceback
        pygame.quit()
        return False

    def run(self) -> None:
        while self._running:
            self._check_event()
            self._update()
            self._draw()

    def _check_event(self) -> None:
        self._current_screen = self._current_screen.handle_event()

        def _quitable():
            return event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_q
            )

        for event in pygame.event.get():
            if _quitable():
                self._running = False

    def _update(self) -> None:
        self._current_screen.update()
        pygame.display.update()

    def _draw(self) -> None:
        self.ctx.surface.fill(Colors.GREY)
        self._current_screen.draw()

import pygame
from torch import Callable

from ai_simulations.ai.neural_net import NeuralNetwork
from ai_simulations.common import Context
from ai_simulations.drawings import Button
from ai_simulations.screens.screen import Screen
from ai_simulations.screens.simulation_screen import SimulationScreen
from ai_simulations.simulations.pendulum_simulation import PendulumSimulation

ScreenFactoryFn = Callable[[], Screen]


class Menu(Screen):
    def __init__(self, ctx: Context) -> None:
        super().__init__(ctx)
        self._buttons: list[tuple[Button, ScreenFactoryFn]] = []
        _simulation = PendulumSimulation(nodes=1, pendulum_length=50, damping=0.25)
        self._buttons.append(
            (
                Button(10, 10, 100, 50, "Pendulum"),
                lambda: SimulationScreen(
                    simulation=_simulation,
                    model=NeuralNetwork(
                        _simulation.input_dim,
                        [16, 16, 16],
                        _simulation.output_dim,
                    ).to("cuda"),
                    ctx=self.ctx,
                ),
            )
        )

    def handle_event(self) -> Screen:
        for button, make_screen in self._buttons:
            if button.mouse_in_area() and pygame.mouse.get_pressed()[0]:
                return make_screen()
        return self

    def update(self) -> None:
        pass

    def draw(self) -> None:
        for button, _ in self._buttons:
            button.draw(self.ctx)

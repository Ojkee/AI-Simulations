from typing import Self

import pygame
import torch
import torch.nn.functional as F
from torch.distributions import Categorical

from ai_simulations.ai import AIModel
from ai_simulations.common import Context
from ai_simulations.screens import Screen
from ai_simulations.simulations import Simulation


class SimulationScreen(Screen):
    def __init__(
        self,
        simulation: Simulation,
        model: AIModel,
        ctx: Context,
    ) -> None:
        super().__init__(ctx)
        self._simulation = simulation
        self._model = model
        self._ctx = ctx

        self.training = False
        self._steps_per_simulation = 3000
        self._epochs = 25
        self._eval_step = self._epochs // 5

        self._simulation.reset()

    def handle_event(self) -> Self:
        state = self._simulation.input_state_vector
        logits = self._model(state.to("cuda"))
        action = Categorical(logits=logits).sample()
        self._simulation.handle_output_vector(
            F.one_hot(action, self._simulation.output_dim)
        )

        self._user_control()
        return self

    def update(self) -> None:
        if self.training:
            self.train_model()
            self.switch_train()

        self._simulation.update()

    def draw(self) -> None:
        self._simulation.draw(self.ctx)
        self._model.draw(self.ctx, (0, self.ctx.height // 2))

    def _user_control(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    self.switch_train()
                elif event.key == pygame.K_r:
                    self._simulation.reset()

    def train_model(self) -> None:
        GAMMA = 0.99
        UPDATE_EVERY = 50
        for epoch in range(self._epochs):
            self._simulation.reset()
            self._run_episode(GAMMA, UPDATE_EVERY)
            if epoch % self._eval_step == 0:
                print(f"{epoch:>3}/{self._epochs}")

        print(f"{self._epochs:>3}/{self._epochs}")

    def _run_episode(self, gamma: float, update_every: int) -> None:
        log_probs, rewards = [], []
        for step in range(self._steps_per_simulation):
            state = self._simulation.input_state_vector
            logits = self._model(state.to("cuda"))
            dist = Categorical(logits=logits)
            action = dist.sample()
            log_probs.append(dist.log_prob(action))

            self._simulation.handle_output_vector(
                F.one_hot(action, self._simulation.output_dim)
            )
            self._simulation.update()
            rewards.append(self._simulation.reward(self._ctx))

            if len(rewards) == update_every or step == self._steps_per_simulation - 1:
                self._update_from_window(log_probs, rewards, gamma)
                log_probs, rewards = [], []

    def _update_from_window(
        self,
        log_probs: list[torch.Tensor],
        rewards: list[torch.Tensor],
        gamma: float,
    ) -> None:
        returns = []
        G = torch.tensor(0.0)
        for r in reversed(rewards):
            G = r + gamma * G
            returns.insert(0, G)
        returns = torch.stack(returns)
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)
        loss = -torch.sum(torch.stack(log_probs) * returns.to("cuda"))
        self._model.update(loss)

    def switch_train(self):
        self.training = not self.training
        self._simulation.reset()

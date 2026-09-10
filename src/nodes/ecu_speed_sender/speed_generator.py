from __future__ import annotations

import math


class SpeedGenerator:
    """Generate a deterministic synthetic vehicle drive cycle."""

    def __init__(
        self,
        max_speed_kph: float = 120.0,
        acceleration_kph_per_step: float = 2.0,
    ) -> None:

        self.max_speed_kph = max_speed_kph
        self.acceleration = acceleration_kph_per_step

        self.speed = 0.0
        self.step = 0

    def next_speed(self) -> float:

        phase = self.step % 120

        if phase < 30:
            self.speed += self.acceleration

        elif phase < 60:
            self.speed += 0.0

        elif phase < 90:
            self.speed -= self.acceleration

        else:
            self.speed = 0.0

        self.speed = max(
            0.0,
            min(self.speed, self.max_speed_kph),
        )

        self.step += 1

        return round(self.speed, 2)

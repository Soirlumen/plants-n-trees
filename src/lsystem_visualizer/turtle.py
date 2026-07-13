from __future__ import annotations

import copy
from dataclasses import dataclass

import numpy as np

from .geometry import normalize, rotate_vector


@dataclass
class TurtleState:
    pos: np.ndarray
    H: np.ndarray
    L: np.ndarray
    U: np.ndarray
    length: float
    radius: float

    @classmethod
    def initial(cls, start_length: float, start_radius: float) -> TurtleState:
        return cls(
            pos=np.array([0.0, 0.0, 0.0]),
            H=np.array([0.0, 1.0, 0.0]),
            L=np.array([-1.0, 0.0, 0.0]),
            U=np.array([0.0, 0.0, 1.0]),
            length=start_length,
            radius=start_radius,
        )

    def copy(self) -> TurtleState:
        return copy.deepcopy(self)

    def orthonormalize(self) -> None:
        """Upraví vektory H, L, U tak, aby byly ortonormální a přesné."""
        self.H = normalize(self.H)
        self.L = self.L - self.H * float(np.dot(self.L, self.H))
        self.L = normalize(self.L)
        self.U = normalize(np.cross(self.H, self.L))
        self.L = normalize(np.cross(self.U, self.H))

    def rotate(
        self, axis_name: str, angle_rad: float, rotated_axes: tuple[str, str]
    ) -> None:
        """Otočí vybrané osy želvy kolem jedné z jejích aktuálních os."""
        axis = getattr(self, axis_name)
        for axis_to_rotate in rotated_axes:
            value = getattr(self, axis_to_rotate)
            rotated = rotate_vector(value, angle_rad, axis.tolist())
            setattr(self, axis_to_rotate, rotated)
        self.orthonormalize()

    def forward(
        self, shrink_length: float, shrink_radius: float
    ) -> tuple[np.ndarray, np.ndarray]:
        """Posune želvu dopředu, zmenší rozměry a vrátí (start, end) segmentu."""
        start = self.pos
        end = start + self.H * self.length

        self.pos = end
        self.length *= shrink_length
        self.radius *= shrink_radius

        return start, end

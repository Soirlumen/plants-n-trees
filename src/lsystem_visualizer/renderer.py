import numpy as np
import trimesh

from .colors import apply_color
from .config import LSystemConfig
from .geometry import sample_angle_rad
from .grammar import LSystemGrammar, Rule
from .meshes import create_leaf_pair
from .presets import TREE
from .turtle import TurtleState


class LSystemRenderer:
    """Třída, která zajišťuje vykreslení L-systému do 3D meshe."""

    def __init__(self, config: LSystemConfig):
        self.config = config
        self.rnd = np.random.default_rng(config.seed)
        self.meshes: list[trimesh.Trimesh] = []
        self.stack: list[TurtleState] = []

    def build(self) -> trimesh.Trimesh:
        """Převede větu na 3D objekt"""
        rules = dict(TREE.rules) if self.config.rules is None else self.config.rules
        grammar = LSystemGrammar(
            axiom=self.config.axiom,
            rules=rules,
        )
        sentence = grammar.expand(
            iterations=self.config.iterations,
            rng=self.rnd,
        )
        state = TurtleState.initial(
            start_length=self.config.start_length,
            start_radius=self.config.start_radius,
        )

        for char in sentence:
            state = self._handle_symbol(char, state)
        if not self.meshes:
            raise ValueError("L-system nic nevygeneroval..")
        return trimesh.util.concatenate(self.meshes)

    def _handle_symbol(self, char: str, state: TurtleState) -> TurtleState:
        """Zpracuje jeden symbol L-systému a vrátí nový stav želvy."""
        if char == "F":
            self._draw_branch(state)

        elif char == "+":
            self._rotate(state, "U", 1, ("H", "L"))

        elif char == "-":
            self._rotate(state, "U", -1, ("H", "L"))

        elif char == "&":
            self._rotate(state, "L", 1, ("H", "U"))

        elif char == "^":
            self._rotate(state, "L", -1, ("H", "U"))

        elif char == "\\":
            self._rotate(state, "H", 1, ("L", "U"))

        elif char == "/":
            self._rotate(state, "H", -1, ("L", "U"))

        elif char == "|":
            state.rotate("U", np.pi, ("H", "L"))

        elif char == "[":
            self.stack.append(state.copy())

        elif char == "]":
            if not self.stack:
                raise ValueError("L-system obsahuje ']', ale stack je prázdný.")
            state = self.stack.pop()

        elif char == "X":
            self._draw_leaf_pair(state)

        return state

    def _draw_branch(self, state: TurtleState) -> None:
        start, end = state.forward(self.config.shrink_length, self.config.shrink_radius)
        cylinder = trimesh.creation.cylinder(
            radius=state.radius,
            segment=[start, end],
            sections=self.config.sections,
        )
        cylinder = apply_color(cylinder, self.config.branch_color)
        self.meshes.append(cylinder)

    def _draw_leaf_pair(self, state: TurtleState):
        """Vykreslí pár listů na konci větve."""
        if not self.config.leaves:
            return
        leaf_pair = create_leaf_pair(
            position=state.pos,
            branch_direction=state.H,
            length=self.config.leaf_length,
            width=self.config.leaf_width,
            fork_angle_degrees=self.config.leaf_fork_angle,
            color_name=self.config.leaf_color,
        )
        self.meshes.append(leaf_pair)

    def _rotate(
        self,
        state: TurtleState,
        axis_name: str,
        sign: int,
        rotated_axes: tuple[str, str],
    ) -> None:
        angle_rad = sample_angle_rad(
            self.config.angle_degrees,
            self.config.stochasticity,
            self.rnd,
        )

        state.rotate(axis_name, sign * angle_rad, rotated_axes)


def build_lsystem_mesh_from_config(config: LSystemConfig) -> trimesh.Trimesh:
    """Převede L-system řetězec na jeden výsledný 3D mesh podle konfigurace."""
    return build_lsystem_mesh(
        iterations=config.iterations,
        angle_degrees=config.angle_degrees,
        shrink_length=config.shrink_length,
        shrink_radius=config.shrink_radius,
        axiom=config.axiom,
        rules=config.rules,
        start_length=config.start_length,
        start_radius=config.start_radius,
        sections=config.sections,
        seed=config.seed,
        stochasticity=config.stochasticity,
        branch_color=config.branch_color,
        leaves=config.leaves,
        leaf_length=config.leaf_length,
        leaf_width=config.leaf_width,
        leaf_fork_angle=config.leaf_fork_angle,
        leaf_color=config.leaf_color,
    )


def build_lsystem_mesh(
    iterations: int = 4,
    angle_degrees: float = 27.0,
    shrink_length: float = 0.95,
    shrink_radius: float = 0.95,
    axiom: str = "X",
    rules: dict[str, Rule] | None = None,
    start_length: float = 0.9,
    start_radius: float = 0.1,
    sections: int = 5,
    seed: int | None = None,
    stochasticity: float = 0.0,
    branch_color: str = "bark",
    leaves: bool = True,
    leaf_length: float = 0.35,
    leaf_width: float = 0.18,
    leaf_fork_angle: float = 40.0,
    leaf_color: str = "leaf",
) -> trimesh.Trimesh:
    config = LSystemConfig(
        iterations=iterations,
        angle_degrees=angle_degrees,
        shrink_length=shrink_length,
        shrink_radius=shrink_radius,
        axiom=axiom,
        rules=rules,
        start_length=start_length,
        start_radius=start_radius,
        sections=sections,
        seed=seed,
        stochasticity=stochasticity,
        branch_color=branch_color,
        leaves=leaves,
        leaf_length=leaf_length,
        leaf_width=leaf_width,
        leaf_fork_angle=leaf_fork_angle,
        leaf_color=leaf_color,
    )

    return LSystemRenderer(config).build()

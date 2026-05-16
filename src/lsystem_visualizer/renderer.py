from .grammar import Rule, expand_lsystem
from .presets import TREE
from .colors import apply_color
from .geometry import rotate_vector, sample_angle_rad
from .meshes import create_leaf_pair,create_needle_cluster
import copy
import numpy as np
import trimesh


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
    leaves: bool = True,
    leaf_length: float = 0.35,
    leaf_width: float = 0.18,
    leaf_fork_angle: float = 40.0,
    leaf_color: str = "leaf",
    needle_length: float = 0.28,
    needle_radius: float = 0.01,
    needle_count: int = 8,
    needle_color: str = "needle",
) -> trimesh.Trimesh:
    rng = np.random.default_rng(seed)

    if rules is None:
        rules = TREE[2]

    sentence = expand_lsystem(
        iterations=iterations,
        axiom=axiom,
        rules=rules,
        rng=rng,
    )

    state = {
        "pos": np.array([0.0, 0.0, 0.0]),
        "dir": np.array([0.0, 1.0, 0.0]),
        "length": start_length,
        "radius": start_radius,
    }

    stack = []
    meshes = []

    for char in sentence:
        if char == "F":
            start = state["pos"]
            end = start + state["dir"] * state["length"]

            cylinder = trimesh.creation.cylinder(
                radius=state["radius"],
                segment=[start, end],
                sections=sections,
            )
            cylinder = apply_color(cylinder, "bark")

            meshes.append(cylinder)
            state["pos"] = end
            state["length"] *= shrink_length
            state["radius"] *= shrink_radius

        elif char == "+":
            angle_rad = sample_angle_rad(angle_degrees, stochasticity, rng)
            state["dir"] = rotate_vector(state["dir"], angle_rad, [0, 0, 1])

        elif char == "-":
            angle_rad = sample_angle_rad(angle_degrees, stochasticity, rng)
            state["dir"] = rotate_vector(state["dir"], -angle_rad, [0, 0, 1])

        elif char == "&":
            angle_rad = sample_angle_rad(angle_degrees, stochasticity, rng)
            state["dir"] = rotate_vector(state["dir"], angle_rad, [1, 0, 0])

        elif char == "^":
            angle_rad = sample_angle_rad(angle_degrees, stochasticity, rng)
            state["dir"] = rotate_vector(state["dir"], -angle_rad, [1, 0, 0])

        elif char == "[":
            stack.append(copy.deepcopy(state))

        elif char == "]":
            if not stack:
                msg = "L-system obsahuje ']', ale stack je prázdný."
                raise ValueError(msg)

            state = stack.pop()

        elif char == "X":
            if leaves:
                leaf_pair = create_leaf_pair(
                    position=state["pos"],
                    branch_direction=state["dir"],
                    length=leaf_length,
                    width=leaf_width,
                    fork_angle_degrees=leaf_fork_angle,
                    color_name=leaf_color,
                )
                meshes.append(leaf_pair)
        elif char == "N":
            needle_cluster = create_needle_cluster(
                position=state["pos"],
                branch_direction=state["dir"],
                rng=rng,
                count=needle_count,
                length=needle_length,
                radius=needle_radius,
                color_name=needle_color,
            )
            meshes.append(needle_cluster)

        elif char in {"X", "A", "B"}:
            pass

    if not meshes:
        msg = "L-system nevygeneroval žádné segmenty. Chybí symbol 'F'?"
        raise ValueError(msg)

    return trimesh.util.concatenate(meshes)


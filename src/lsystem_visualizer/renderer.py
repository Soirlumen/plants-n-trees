import copy

import numpy as np
import trimesh

from .colors import apply_color
from .geometry import normalize, rotate_vector, sample_angle_rad
from .grammar import Rule, expand_lsystem
from .meshes import create_leaf_pair
from .presets import TREE


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
) -> trimesh.Trimesh:
    rng = np.random.default_rng(seed)

    active_rules: dict[str, Rule] = dict(TREE[2]) if rules is None else rules

    sentence = expand_lsystem(
        iterations=iterations,
        axiom=axiom,
        rules=active_rules,
        rng=rng,
    )

    state = {
        "pos": np.array([0.0, 0.0, 0.0]),
        "H": np.array([0.0, 1.0, 0.0]),
        "L": np.array([-1.0, 0.0, 0.0]),
        "U": np.array([0.0, 0.0, 1.0]),
        "length": start_length,
        "radius": start_radius,
    }

    stack = []
    meshes = []

    for char in sentence:
        if char == "F":
            start = state["pos"]
            end = start + state["H"] * state["length"]

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
            rotate_turtle(state, "U", angle_rad, ("H", "L"))

        elif char == "-":
            angle_rad = sample_angle_rad(angle_degrees, stochasticity, rng)
            rotate_turtle(state, "U", -angle_rad, ("H", "L"))

        elif char == "&":
            angle_rad = sample_angle_rad(angle_degrees, stochasticity, rng)
            rotate_turtle(state, "L", angle_rad, ("H", "U"))

        elif char == "^":
            angle_rad = sample_angle_rad(angle_degrees, stochasticity, rng)
            rotate_turtle(state, "L", -angle_rad, ("H", "U"))

        elif char == "\\":
            angle_rad = sample_angle_rad(angle_degrees, stochasticity, rng)
            rotate_turtle(state, "H", angle_rad, ("L", "U"))

        elif char == "/":
            angle_rad = sample_angle_rad(angle_degrees, stochasticity, rng)
            rotate_turtle(state, "H", -angle_rad, ("L", "U"))

        elif char == "|":
            rotate_turtle(state, "U", np.pi, ("H", "L"))

        # --- UKLÁDÁNÍ STAVU ---
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
                    branch_direction=state["H"],
                    length=leaf_length,
                    width=leaf_width,
                    fork_angle_degrees=leaf_fork_angle,
                    color_name=leaf_color,
                )
                meshes.append(leaf_pair)

        elif char in {"A"}:
            pass

    if not meshes:
        msg = "L-system nevygeneroval žádné segmenty."
        raise ValueError(msg)

    return trimesh.util.concatenate(meshes)


def orthonormalize_turtle(state: dict) -> None:
    heading = normalize(state["H"])

    left = state["L"] - heading * float(np.dot(state["L"], heading))
    left = normalize(left)

    up = normalize(np.cross(heading, left))
    left = normalize(np.cross(up, heading))

    state["H"] = heading
    state["L"] = left
    state["U"] = up


def rotate_turtle(
    state: dict,
    axis_key: str,
    angle_rad: float,
    rotated_keys: tuple[str, str],
) -> None:
    axis = state[axis_key]

    for key in rotated_keys:
        state[key] = rotate_vector(
            state[key],
            angle_rad,
            axis.tolist(),
        )

    orthonormalize_turtle(state)

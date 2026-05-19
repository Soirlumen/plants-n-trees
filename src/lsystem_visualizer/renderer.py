import copy

import numpy as np
import trimesh

from .colors import apply_color
from .geometry import normalize, rotate_vector, sample_angle_rad
from .grammar import Rule, expand_lsystem
from .meshes import create_leaf_pair
from .presets import TREE


def orthonormalize_turtle(state: dict) -> None:
    """Srovná lokální osy želvy tak, aby zůstaly kolmé a jednotkové."""
    heading = normalize(state["H"])

    # Po hodně rotacích se kvůli zaokrouhlování může báze lehce rozhodit.
    # Tady left očistíme o složku ve směru headingu a znovu dopočítáme up.
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
    """Otočí vybrané osy želvy kolem jedné z jejích aktuálních os"""
    axis = state[axis_key]

    for key in rotated_keys:
        state[key] = rotate_vector(
            state[key],
            angle_rad,
            axis.tolist(),
        )

    orthonormalize_turtle(state)


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
    """Převede L-system řetězec na jeden výsledný 3D mesh."""
    rng = np.random.default_rng(seed)

    # Když volající nedodá vlastní pravidla, použije se jednoduchý výchozí strom
    active_rules: dict[str, Rule] = dict(TREE[2]) if rules is None else rules

    sentence = expand_lsystem(
        iterations=iterations,
        axiom=axiom,
        rules=active_rules,
        rng=rng,
    )

    # Turtle stav: pozice, tři lokální osy a aktuální rozměry větve.
    # H = heading/směr dopředu, L = levá osa, U = osa nahoru.
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

            # Každé F vytvoří jeden válcový segment ve směru aktuální želvy.
            cylinder = trimesh.creation.cylinder(
                radius=state["radius"],
                segment=[start, end],
                sections=sections,
            )
            cylinder = apply_color(cylinder, branch_color)

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

        elif char == "[":
            # Větvení: uložíme celý stav, aby se po dokončení větve dalo vrátit zpet.
            stack.append(copy.deepcopy(state))

        elif char == "]":
            if not stack:
                msg = "L-system obsahuje ']', ale stack je prázdný."
                raise ValueError(msg)
            state = stack.pop()

        elif char == "X":
            # X nekreslí větev. Bereme ho jako růstový bod, kam lze přidat listy.
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

    if not meshes:
        msg = "L-system nevygeneroval žádné segmenty."
        raise ValueError(msg)

    return trimesh.util.concatenate(meshes)

import argparse
import copy

import numpy as np
import trimesh
from trimesh.transformations import rotation_matrix

Rule = str | list[tuple[float, str]]
Color = tuple[int, int, int, int]

COLORS: dict[str, Color] = {
    "bark": (92, 64, 45, 255),
    "bark_dark": (60, 40, 28, 255),
    "leaf": (34, 139, 34, 255),
    "leaf_light": (80, 180, 70, 255),
    "leaf_dark": (20, 100, 30, 255),
    "needle": (20, 80, 35, 255),
    "needle_light": (40, 130, 55, 255),
}

CONIFER_TREE = (
    7,
    "FFFA",
    {
        "A": "F[+B][-B][&B][^B]A",
        "B": "F[+N][-N][&N][^N]N",
        "F": "F",
    },
)

GRASS = (
    4,
    "X",
    {
        "F": "FF",
        "X": "F-[[X]+X]+F[+FX]-X",
    },
)

TREE = (
    4,
    "X",
    {
        "X": "F[+X][-X][&X][^X]FX",
        "F": "FF",
    },
)

STOCHASTIC_TREE = (
    4,
    "X",
    {
        "X": [
            (0.50, "F[+X][-X]FX"),
            (0.30, "F[+X][-X][&X]FX"),
            (0.20, "F[+X][-X][&X][^X]FX"),
        ],
        "F": [
            (0.85, "FF"),
            (0.15, "F"),
        ],
    },
)

OAK_TREE = (
    5,
    "FFFFX",
    {
        "F": "F",
        "X": [
            (0.35, "F[+X][-X]FX"),
            (0.25, "F[&X][^X]FX"),
            (0.25, "F[+X][&X]F[-X][^X]X"),
            (0.15, "FFX"),
        ],
    },
)

PRESETS = {
    "grass": GRASS,
    "tree": TREE,
    "stochastic-tree": STOCHASTIC_TREE,
    "oak-tree": OAK_TREE,
    "conifer-tree": CONIFER_TREE,
}


def apply_color(mesh: trimesh.Trimesh, color_name: str) -> trimesh.Trimesh:
    mesh.visual.face_colors = COLORS[color_name]
    return mesh


def create_leaf(
    position: np.ndarray,
    radius: float = 0.08,
) -> trimesh.Trimesh:
    leaf = trimesh.creation.icosphere(
        subdivisions=2,
        radius=radius,
    )

    leaf.apply_translation(position)

    leaf.visual.face_colors = [34, 139, 34, 255]  # zelená RGBA

    return leaf


def choose_replacement(rule: Rule, rng: np.random.Generator) -> str:
    if isinstance(rule, str):
        return rule

    weights = np.array([weight for weight, _ in rule], dtype=float)
    weights /= weights.sum()

    index = rng.choice(len(rule), p=weights)
    return rule[index][1]


def expand_lsystem(
    iterations: int,
    axiom: str,
    rules: dict[str, Rule],
    rng: np.random.Generator,
) -> str:
    result = axiom

    for _ in range(iterations):
        new_result = []

        for symbol in result:
            rule = rules.get(symbol, symbol)
            new_result.append(choose_replacement(rule, rng))

        result = "".join(new_result)

    return result


def normalize(vector: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vector)

    if norm == 0:
        return vector

    return vector / norm


def get_perpendicular_basis(direction: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    direction = normalize(direction)

    helper = np.array([0.0, 0.0, 1.0])

    if abs(np.dot(direction, helper)) > 0.95:
        helper = np.array([1.0, 0.0, 0.0])

    side = normalize(np.cross(direction, helper))
    up = normalize(np.cross(side, direction))

    return side, up


def create_diamond_leaf(
    position: np.ndarray,
    direction: np.ndarray,
    width_axis: np.ndarray,
    length: float = 0.35,
    width: float = 0.18,
    color_name: str = "leaf",
) -> trimesh.Trimesh:
    direction = normalize(direction)
    width_axis = normalize(width_axis)

    base = position
    center = position + direction * (length * 0.5)
    tip = position + direction * length

    left = center + width_axis * (width * 0.5)
    right = center - width_axis * (width * 0.5)

    vertices = np.array(
        [
            tip,
            right,
            base,
            left,
        ],
    )

    faces = np.array(
        [
            [0, 1, 2],
            [0, 2, 3],
            [2, 1, 0],
            [3, 2, 0],
        ],
    )

    leaf = trimesh.Trimesh(
        vertices=vertices,
        faces=faces,
        process=False,
    )

    return apply_color(leaf, color_name)


def create_leaf_pair(
    position: np.ndarray,
    branch_direction: np.ndarray,
    length: float = 0.35,
    width: float = 0.18,
    fork_angle_degrees: float = 35.0,
    color_name: str = "leaf",
) -> trimesh.Trimesh:
    branch_direction = normalize(branch_direction)
    _, up = get_perpendicular_basis(branch_direction)

    fork_angle_rad = np.radians(fork_angle_degrees)

    left_direction = rotate_vector(
        branch_direction,
        fork_angle_rad,
        up.tolist(),
    )
    right_direction = rotate_vector(
        branch_direction,
        -fork_angle_rad,
        up.tolist(),
    )

    leaf_1 = create_diamond_leaf(
        position=position,
        direction=left_direction,
        width_axis=up,
        length=length,
        width=width,
        color_name=color_name,
    )

    leaf_2 = create_diamond_leaf(
        position=position,
        direction=right_direction,
        width_axis=up,
        length=length,
        width=width,
        color_name=color_name,
    )

    return trimesh.util.concatenate([leaf_1, leaf_2])


def rotate_vector(
    direction: np.ndarray,
    angle_rad: float,
    axis: list[float],
) -> np.ndarray:
    rotation = rotation_matrix(angle_rad, axis)
    return rotation[:3, :3] @ direction


def sample_angle_rad(
    angle_degrees: float,
    stochasticity: float,
    rng: np.random.Generator,
) -> float:
    angle_noise = rng.normal(loc=0.0, scale=stochasticity)
    return np.radians(angle_degrees + angle_noise)


def create_needle_cluster(
    position: np.ndarray,
    branch_direction: np.ndarray,
    rng: np.random.Generator,
    count: int = 8,
    length: float = 0.28,
    radius: float = 0.01,
    spread: float = 0.75,
    color_name: str = "needle",
) -> trimesh.Trimesh:
    branch_direction = normalize(branch_direction)
    side, up = get_perpendicular_basis(branch_direction)

    meshes = []
    angle_offset = rng.uniform(0.0, 2.0 * np.pi)

    for index in range(count):
        angle = angle_offset + 2.0 * np.pi * index / count

        radial_direction = np.cos(angle) * side + np.sin(angle) * up

        needle_direction = normalize(
            branch_direction * 0.65 + radial_direction * spread
        )

        start = position
        end = position + needle_direction * length

        needle = trimesh.creation.cylinder(
            radius=radius,
            segment=[start, end],
            sections=4,
        )

        needle = apply_color(needle, color_name)
        meshes.append(needle)

    return trimesh.util.concatenate(meshes)


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--preset",
        choices=PRESETS.keys(),
        default="tree",
    )
    parser.add_argument("--iterations", type=int, default=None)
    parser.add_argument("--angle", type=float, default=27.0)
    parser.add_argument("--shrink-length", type=float, default=0.95)
    parser.add_argument("--shrink-radius", type=float, default=0.95)
    parser.add_argument("--output", type=str, default="tree.obj")
    parser.add_argument("--show", action="store_true")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--stochasticity", type=float, default=0.0)
    parser.add_argument("--no-leaves", action="store_true")
    parser.add_argument("--leaf-length", type=float, default=0.35)
    parser.add_argument("--leaf-width", type=float, default=0.18)
    parser.add_argument("--leaf-fork-angle", type=float, default=40.0)
    parser.add_argument("--leaf-color", choices=COLORS.keys(), default="leaf")
    parser.add_argument("--needle-length", type=float, default=0.28)
    parser.add_argument("--needle-radius", type=float, default=0.01)
    parser.add_argument("--needle-count", type=int, default=8)
    parser.add_argument("--needle-color", choices=COLORS.keys(), default="needle")

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    preset_iterations, axiom, rules = PRESETS[args.preset]
    iterations = args.iterations if args.iterations is not None else preset_iterations

    tree_mesh = build_lsystem_mesh(
        iterations=iterations,
        angle_degrees=args.angle,
        shrink_length=args.shrink_length,
        shrink_radius=args.shrink_radius,
        axiom=axiom,
        rules=rules,
        seed=args.seed,
        stochasticity=args.stochasticity,
        leaves=not args.no_leaves,
        leaf_length=args.leaf_length,
        leaf_width=args.leaf_width,
        leaf_fork_angle=args.leaf_fork_angle,
        leaf_color=args.leaf_color,
        needle_length=args.needle_length,
        needle_radius=args.needle_radius,
        needle_count=args.needle_count,
        needle_color=args.needle_color,
    )

    tree_mesh.export(args.output)
    print(f"Exportováno do: {args.output}")

    if args.show:
        scene = trimesh.Scene([tree_mesh])
        scene.show()


if __name__ == "__main__":
    main()

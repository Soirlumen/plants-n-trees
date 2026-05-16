import numpy as np
import trimesh
from .geometry import normalize, get_perpendicular_basis, rotate_vector
from .colors import apply_color

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


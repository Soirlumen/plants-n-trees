import numpy as np
import trimesh

from .colors import apply_color
from .geometry import get_perpendicular_basis, normalize, rotate_vector


def create_diamond_leaf(
    position: np.ndarray,
    direction: np.ndarray,
    width_axis: np.ndarray,
    length: float = 0.35,
    width: float = 0.18,
    color_name: str = "leaf",
) -> trimesh.Trimesh:
    """Vytvoří kosočtverec ze 4 bodů jako list."""
    direction = normalize(direction)
    width_axis = normalize(width_axis)

    # List stavíme z bodu na větvi: základna, střed, špička a dva boční body.
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

    # Dvě přední a dvě zadní plochy, aby byl list viditelný z obou stran
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
    """Vytvoří dvojici listů roztaženou do stran od směru větve pro víc živý nádech."""
    branch_direction = normalize(branch_direction)

    # Potřebujeme osu kolem které listy rozevřeme. Helper volíme tak,
    # aby nebyl skoro rovnoběžný se směrem větve.
    helper = np.array([0.0, 0.0, 1.0])
    if abs(np.dot(branch_direction, helper)) > 0.95:
        helper = np.array([1.0, 0.0, 0.0])
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

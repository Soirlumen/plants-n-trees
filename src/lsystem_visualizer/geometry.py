import numpy as np
from trimesh.transformations import rotation_matrix


def normalize(vector: np.ndarray) -> np.ndarray:
    """Vrátí vektor stejného směru s délkou 1."""
    norm = np.linalg.norm(vector)

    # Nulový vektor nemá směr. Necháme ho být, místo aby vzniklo dělení nulou
    if norm == 0:
        return vector

    return vector / norm


def rotate_vector(
    direction: np.ndarray,
    angle_rad: float,
    axis: list[float],
) -> np.ndarray:
    """Otočí vektor kolem zadané osy o úhel v radiánech."""
    rotation = rotation_matrix(angle_rad, axis)
    return rotation[:3, :3] @ direction


def get_perpendicular_basis(direction: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Najde dvě kolmé osy k danému směru."""
    direction = normalize(direction)

    helper = np.array([0.0, 0.0, 1.0])

    # Když direction míří skoro stejně jako helper, cross product by byl moc malý,
    # proto v takovém případě sáhneme po jiné pomocné ose
    if abs(np.dot(direction, helper)) > 0.95:
        helper = np.array([1.0, 0.0, 0.0])

    side = normalize(np.cross(direction, helper))
    up = normalize(np.cross(side, direction))

    return side, up


def sample_angle_rad(
    angle_degrees: float,
    stochasticity: float,
    rng: np.random.Generator,
) -> float:
    """Vrátí úhel v radiánech, případně s malou náhodnou odchylkou."""
    angle_noise = rng.normal(loc=0.0, scale=stochasticity)
    return np.radians(angle_degrees + angle_noise)

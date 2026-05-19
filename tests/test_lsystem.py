import numpy as np
import pytest
import trimesh

from lsystem_visualizer.colors import apply_color
from lsystem_visualizer.geometry import (
    get_perpendicular_basis,
    normalize,
    rotate_vector,
    sample_angle_rad,
)
from lsystem_visualizer.grammar import choose_replacement, expand_lsystem
from lsystem_visualizer.meshes import create_diamond_leaf
from lsystem_visualizer.renderer import build_lsystem_mesh, rotate_turtle


def test_choose_replacement_returns_plain_string_rule():
    rng = np.random.default_rng(0)

    result = choose_replacement("FF", rng)

    assert result == "FF"


def test_choose_replacement_respects_certain_weighted_rule():
    rng = np.random.default_rng(0)
    rule = [
        (0.0, "A"),
        (1.0, "B"),
    ]

    result = choose_replacement(rule, rng)

    assert result == "B"


def test_expand_lsystem_keeps_symbols_without_rule():
    rng = np.random.default_rng(0)
    rules = {"F": "FF"}

    result = expand_lsystem(
        iterations=2,
        axiom="F+X",
        rules=rules,
        rng=rng,
    )

    assert result == "FFFF+X"


def test_expand_lsystem_zero_iterations_returns_axiom():
    rng = np.random.default_rng(0)

    result = expand_lsystem(
        iterations=0,
        axiom="X+F",
        rules={"X": "F"},
        rng=rng,
    )

    assert result == "X+F"


def test_normalize_zero_vector_returns_zero_vector():
    vector = np.array([0.0, 0.0, 0.0])

    result = normalize(vector)

    np.testing.assert_allclose(result, vector)


def test_normalize_nonzero_vector_has_unit_length():
    vector = np.array([3.0, 4.0, 0.0])

    result = normalize(vector)

    np.testing.assert_allclose(np.linalg.norm(result), 1.0)
    np.testing.assert_allclose(result, np.array([0.6, 0.8, 0.0]))


def test_rotate_vector_around_z_axis_by_90_degrees():
    direction = np.array([1.0, 0.0, 0.0])

    result = rotate_vector(
        direction=direction,
        angle_rad=np.pi / 2,
        axis=[0.0, 0.0, 1.0],
    )

    np.testing.assert_allclose(result, np.array([0.0, 1.0, 0.0]), atol=1e-7)


def test_get_perpendicular_basis_returns_orthonormal_vectors():
    direction = np.array([0.0, 0.0, 1.0])

    side, up = get_perpendicular_basis(direction)

    np.testing.assert_allclose(np.linalg.norm(side), 1.0)
    np.testing.assert_allclose(np.linalg.norm(up), 1.0)
    np.testing.assert_allclose(np.dot(side, direction), 0.0, atol=1e-7)
    np.testing.assert_allclose(np.dot(up, direction), 0.0, atol=1e-7)
    np.testing.assert_allclose(np.dot(side, up), 0.0, atol=1e-7)


def test_sample_angle_without_stochasticity_is_exact_angle():
    rng = np.random.default_rng(0)

    result = sample_angle_rad(
        angle_degrees=90.0,
        stochasticity=0.0,
        rng=rng,
    )

    np.testing.assert_allclose(result, np.pi / 2)


def test_apply_color_sets_mesh_face_colors():
    mesh = trimesh.creation.box()

    result = apply_color(mesh, "leaf")

    assert result is mesh
    assert len(result.visual.face_colors) == len(result.faces)
    np.testing.assert_array_equal(
        result.visual.face_colors[0], np.array([34, 139, 34, 255])
    )


def test_create_diamond_leaf_has_expected_geometry():
    leaf = create_diamond_leaf(
        position=np.array([0.0, 0.0, 0.0]),
        direction=np.array([0.0, 1.0, 0.0]),
        width_axis=np.array([1.0, 0.0, 0.0]),
        length=1.0,
        width=0.5,
    )

    assert isinstance(leaf, trimesh.Trimesh)
    assert len(leaf.vertices) == 4
    assert len(leaf.faces) == 4


def test_rotate_turtle_preserves_orthonormal_basis():
    state = {
        "pos": np.array([0.0, 0.0, 0.0]),
        "H": np.array([0.0, 1.0, 0.0]),
        "L": np.array([-1.0, 0.0, 0.0]),
        "U": np.array([0.0, 0.0, 1.0]),
        "length": 1.0,
        "radius": 0.1,
    }

    rotate_turtle(
        state=state,
        axis_key="U",
        angle_rad=np.pi / 3,
        rotated_keys=("H", "L"),
    )

    for key in ("H", "L", "U"):
        np.testing.assert_allclose(np.linalg.norm(state[key]), 1.0)

    np.testing.assert_allclose(np.dot(state["H"], state["L"]), 0.0, atol=1e-7)
    np.testing.assert_allclose(np.dot(state["H"], state["U"]), 0.0, atol=1e-7)
    np.testing.assert_allclose(np.dot(state["L"], state["U"]), 0.0, atol=1e-7)


def test_build_lsystem_mesh_from_single_forward_segment():
    mesh = build_lsystem_mesh(
        iterations=0,
        axiom="F",
        rules={},
        start_length=1.0,
        start_radius=0.1,
        leaves=False,
        sections=6,
    )

    assert isinstance(mesh, trimesh.Trimesh)
    assert len(mesh.vertices) > 0
    assert len(mesh.faces) > 0


def test_build_lsystem_mesh_raises_for_unmatched_closing_bracket():
    with pytest.raises(ValueError, match="stack je prázdný"):
        build_lsystem_mesh(
            iterations=0,
            axiom="]",
            rules={},
            leaves=False,
        )


def test_build_lsystem_mesh_raises_when_no_segments_are_generated():
    with pytest.raises(ValueError, match="nevygeneroval žádné segmenty"):
        build_lsystem_mesh(
            iterations=0,
            axiom="",
            rules={},
            leaves=False,
        )

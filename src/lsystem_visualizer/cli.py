import argparse

import trimesh

from .colors import COLORS
from .presets import PRESETS
from .renderer import build_lsystem_mesh


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--preset",
        choices=PRESETS.keys(),
        default="tree",
    )
    parser.add_argument("--iterations", type=int, default=None)
    parser.add_argument("--angle", type=float, default=27.0)
    parser.add_argument("--shrink-length", type=float, default=0.9)
    parser.add_argument("--shrink-radius", type=float, default=0.85)
    parser.add_argument("--output", type=str, default="tree.obj")
    parser.add_argument("--show", action="store_true")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--stochasticity", type=float, default=0.0)
    parser.add_argument("--no-leaves", action="store_true")
    parser.add_argument("--leaf-length", type=float, default=1.2)
    parser.add_argument("--leaf-width", type=float, default=0.6)
    parser.add_argument("--leaf-fork-angle", type=float, default=40.0)
    parser.add_argument("--leaf-color", choices=COLORS.keys(), default="leaf")
    parser.add_argument("--start-length", type=float, default=0.9)
    parser.add_argument("--start-radius", type=float, default=0.1)

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
        start_length=args.start_length,
        start_radius=args.start_radius,
    )

    tree_mesh.export(args.output)
    print(f"Exportováno do: {args.output}")

    if args.show:
        scene = trimesh.Scene([tree_mesh])
        scene.show()


if __name__ == "__main__":
    main()

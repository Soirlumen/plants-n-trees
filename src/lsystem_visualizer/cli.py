import argparse

import trimesh

from .colors import COLORS
from .presets import PRESETS
from .renderer import LSystemRenderer
from .config import LSystemConfig


def parse_args() -> argparse.Namespace:
    """Načte parametry z příkazové řádky"""
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
    parser.add_argument("--branch-color", choices=COLORS.keys(), default="bark")

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    preset = PRESETS[args.preset]
    iterations = args.iterations if args.iterations is not None else preset.iterations

    config = LSystemConfig(
        iterations=iterations,
        angle_degrees=args.angle,
        shrink_length=args.shrink_length,
        shrink_radius=args.shrink_radius,
        axiom=preset.axiom,
        rules=preset.rules,
        seed=args.seed,
        stochasticity=args.stochasticity,
        leaves=not args.no_leaves,
        leaf_length=args.leaf_length,
        leaf_width=args.leaf_width,
        leaf_fork_angle=args.leaf_fork_angle,
        leaf_color=args.leaf_color,
        start_length=args.start_length,
        start_radius=args.start_radius,
        branch_color=args.branch_color,
    )

    tree_mesh = LSystemRenderer(config).build()

    tree_mesh.export(args.output)
    print(f"Exportováno do: {args.output}")

    if args.show:
        scene = trimesh.Scene([tree_mesh])
        scene.show()


def _run_with_args(args):
    import sys
    sys.argv[1:] = args
    main() 

def nudny_strom():
    _run_with_args(["--preset", "tree", "--iterations", "5", "--angle", "27", "--shrink-length", "0.955", "--shrink-radius", "0.94", "--start-length", "0.36", "--start-radius", "0.11", "--leaf-length", "0.4", "--leaf-width", "0.13", "--leaf-fork-angle", "35", "--stochasticity", "0", "--seed", "23", "--leaf-color", "leaf_light", "--show"])

def strom():
    _run_with_args(["--preset", "dense-stochastic-tree", "--iterations", "7", "--angle", "27", "--shrink-length", "0.955", "--shrink-radius", "0.94", "--start-length", "0.36", "--start-radius", "0.11", "--leaf-length", "0.4", "--leaf-width", "0.13", "--leaf-fork-angle", "35", "--stochasticity", "4.5", "--seed", "23", "--leaf-color", "leaf_light", "--show"])

def jiny_strom():
    _run_with_args(["--preset", "oak-tree", "--iterations", "6", "--angle", "27", "--shrink-length", "0.955", "--shrink-radius", "0.88", "--start-length", "0.36", "--start-radius", "0.08", "--leaf-length", "0.4", "--leaf-width", "0.13", "--leaf-fork-angle", "35", "--stochasticity", "4", "--seed", "22222", "--leaf-color", "leaf_light", "--show"])

def kerik():
    _run_with_args(["--preset", "stochastic-bush", "--seed", "7", "--angle", "32", "--stochasticity", "7", "--iterations", "5", "--start-length", "0.28", "--start-radius", "0.035", "--shrink-length", "0.86", "--shrink-radius", "0.78", "--leaf-length", "0.2", "--leaf-width", "0.10", "--leaf-color", "leaf_dark", "--show"])

def trava():
    _run_with_args(["--preset", "stochastic-grass", "--seed", "12", "--angle", "10", "--stochasticity", "4", "--start-length", "0.22", "--start-radius", "0.012", "--shrink-length", "0.96", "--shrink-radius", "0.88", "--no-leaves", "--output", "ground_grass.obj", "--branch-color", "leaf_dark", "--show"])

def dalsi_strom():
    _run_with_args(["--preset", "dense-stochastic-tree", "--iterations", "6", "--angle", "29", "--shrink-length", "0.94", "--shrink-radius", "0.90", "--start-length", "0.36", "--start-radius", "0.15", "--leaf-length", "0.4", "--leaf-width", "0.15", "--leaf-fork-angle", "35", "--stochasticity", "20", "--seed", "3854", "--leaf-color", "leaf_purple", "--show"])
if __name__ == "__main__":
    main()

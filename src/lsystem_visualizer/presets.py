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
        "X": "F[/+X][\\-X][&X][^X]FX",
        "F": "FF",
    },
)

STOCHASTIC_TREE = (
    4,
    "X",
    {
        "X": [
            (0.50, "F[/+X][\\-X]FX"),
            (0.30, "F[/+X][^X]FX"),
            (0.20, "F[^X][\\-X]FX"),
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
            (0.35, "F[/+X][\\-X]FX"),
            (0.25, "F[&X][^X]FX"),
            (0.25, "F[/+X][&X]F[\\-X][^X]X"),
            (0.15, "FFX"),
        ],
    },
)

DENSE_STOCHASTIC_TREE = (
    6,
    "FX",
    {
        "X": [
            (0.28, "F[/+X][\\-X]F[&X]X"),
            (0.24, "F[&/+X][&\\-X]FX"),
            (0.20, "F[+X][-X][^X]FX"),
            (0.16, "F[/+X][\\&X]F[^X]X"),
            (0.12, "FFX"),
        ],
        "F": [
            (0.72, "F"),
            (0.28, "FF"),
        ],
    },
)


PRESETS = {
    "grass": GRASS,
    "tree": TREE,
    "stochastic-tree": STOCHASTIC_TREE,
    "oak-tree": OAK_TREE,
    "dense-stochastic-tree": DENSE_STOCHASTIC_TREE,
}

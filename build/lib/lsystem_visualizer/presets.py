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

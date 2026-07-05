# Každý preset má stejný tvar: počet iterací, axiom a pravidla přepisování.
# Axiom je startovní řetězec; pravidla pak určují, jak se rostlina rozvětví.
from .config import Preset

TREE = Preset(
    iterations=5,
    axiom="X",
    rules={
        "X": "F[/+X][\\-X][&X][^X]FX",
        "F": "FF",
    },
)

# U stochastických presetů má jeden symbol víc možných náhrad,
# číslo u každé možnosti říká, jak velkou váhu při náhodném výběru má.
STOCHASTIC_TREE = Preset(
    iterations=5,
    axiom="X",
    rules={
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

OAK_TREE = Preset(
    iterations=5,
    axiom="FFFFX",
    rules={
        "F": "F",
        "X": [
            (0.35, "F[/+X][\\-X]FX"),
            (0.25, "F[&X][^X]FX"),
            (0.25, "F[/+X][&X]F[\\-X][^X]X"),
            (0.15, "FFX"),
        ],
    },
)

DENSE_STOCHASTIC_TREE = Preset(
    iterations=6,
    axiom="FX",
    rules={
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

STOCHASTIC_GRASS = Preset(
    iterations=7,
    axiom="[X][+X][-X][&X][^X][/+X][\\-X][/&X][\\^X][+&X][-^X]",
    rules={
        "F": "F",
        "X": [
            (0.26, "F+X"),
            (0.26, "F-X"),
            (0.18, "F&X"),
            (0.18, "F^X"),
            (0.07, "F/+X"),
            (0.03, "F\\-X"),
            (0.02, "F"),
        ],
    },
)

STOCHASTIC_BUSH = Preset(
    iterations=5,
    axiom="[X][+X][-X][&X][^X][/+X][\\-X][+&X][-^X]",
    rules={
        "F": [
            (0.75, "F"),
            (0.25, "FF"),
        ],
        "X": [
            (0.26, "F[+X][-X]X"),
            (0.22, "F[&X][^X]X"),
            (0.20, "F[/+X][\\-X]X"),
            (0.16, "F[+X][&X][-X]"),
            (0.10, "F[/X][\\X]"),
            (0.06, "F[+X][-X][&X][^X]"),
        ],
    },
)

# cli.py pracuje s textovým názvem, renderer pak dostane konkrétní
# trojici presetových hodnot.
PRESETS = {
    "tree": TREE,
    "stochastic-tree": STOCHASTIC_TREE,
    "oak-tree": OAK_TREE,
    "dense-stochastic-tree": DENSE_STOCHASTIC_TREE,
    "stochastic-grass": STOCHASTIC_GRASS,
    "stochastic-bush": STOCHASTIC_BUSH,
}
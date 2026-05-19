# Každý preset má stejný tvar: počet iterací, axiom a pravidla přepisování.
# Axiom je startovní řetězec; pravidla pak určují, jak se rostlina rozvětví.


TREE = (
    5,
    "X",
    {
        "X": "F[/+X][\\-X][&X][^X]FX",
        "F": "FF",
    },
)

# U stochastických presetů má jeden symbol víc možných náhrad,
# číslo u každé možnosti říká, jak velkou váhu při náhodném výběru má.
STOCHASTIC_TREE = (
    5,
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

STOCHASTIC_GRASS = (
    7,
    "[X][+X][-X][&X][^X][/+X][\\-X][/&X][\\^X][+&X][-^X]",
    {
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

STOCHASTIC_BUSH = (
    5,
    "[X][+X][-X][&X][^X][/+X][\\-X][+&X][-^X]",
    {
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

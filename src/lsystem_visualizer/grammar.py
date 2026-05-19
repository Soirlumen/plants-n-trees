import numpy as np

# Pravidlo je buď pevná náhrada nebo seznam možností s pravděpodobnostní vahou.
Rule = str | list[tuple[float, str]]


def choose_replacement(rule: Rule, rng: np.random.Generator) -> str:
    """Vybere text, kterým se nahradí jeden symbol L-systému."""
    if isinstance(rule, str):
        return rule

    # U stochastických pravidel nejdřív převedeme váhy na pravděpodobnosti
    # a díky tomu nemusí ručně dávat součet přesně 1
    weights = np.array([weight for weight, _ in rule], dtype=float)
    weights /= weights.sum()

    index = rng.choice(len(rule), p=weights)
    return rule[index][1]


def expand_lsystem(
    iterations: int,
    axiom: str,
    rules: dict[str, Rule],
    rng: np.random.Generator,
) -> str:
    """Postupně rozepíše axiom podle pravidel do finálního řetězce."""
    result = axiom

    for _ in range(iterations):
        new_result = []

        for symbol in result:
            # symboly bez pravidla necháváme beze změny
            rule = rules.get(symbol, symbol)
            new_result.append(choose_replacement(rule, rng))

        result = "".join(new_result)

    return result

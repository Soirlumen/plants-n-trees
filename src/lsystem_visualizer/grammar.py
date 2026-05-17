import numpy as np

Rule = str | list[tuple[float, str]]


def choose_replacement(rule: Rule, rng: np.random.Generator) -> str:
    if isinstance(rule, str):
        return rule

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
    result = axiom

    for _ in range(iterations):
        new_result = []

        for symbol in result:
            rule = rules.get(symbol, symbol)
            new_result.append(choose_replacement(rule, rng))

        result = "".join(new_result)

    return result

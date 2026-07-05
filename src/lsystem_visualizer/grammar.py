import numpy as np

# Pravidlo je buď pevná náhrada nebo seznam možností s pravd.stní váhou.
Rule = str | list[tuple[float, str]]

class LSystemGrammar:
    def __init__(self,axiom: str, rules: dict[str, Rule]):
        self.axiom = axiom
        self.rules = rules
    def expand(self,iterations:int,rng:np.random.Generator)->str:
        """Postupně rozepíše axiom podle pravidel do finálního řetězce."""
        result=self.axiom
        for _ in range(iterations):
            new_result=[]
            for symbol in result:
                # symboly bez pravidla necháváme beze změny
                rule=self.rules.get(symbol,symbol)
                new_result.append(self._choose_replacement(rule,rng))
            result="".join(new_result)
        return result
    
    def _choose_replacement(self,rule:Rule,rng:np.random.Generator)->str:
        """Vybere text, kterým se nahradí jeden symbol L-systému."""
        if isinstance(rule,str):
            return rule
        # U stoch pravidel nejdřív převedeme váhy na pravd.sti
        # -> nemusí dávát ručně jedna.
        weights=np.array([weight for weight,_ in rule],dtype=float)
        weights/=weights.sum()
        index=rng.choice(len(rule),p=weights)
        return rule[index][1]
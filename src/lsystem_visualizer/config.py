from dataclasses import dataclass
from .grammar import Rule

@dataclass
class LSystemConfig:
     iterations: int=4
     angle_degrees: float=27.0
     shrink_length:float=0.95
     shrink_radius:float=0.95
     
     axiom:str="X"
     rules:dict[str,Rule]| None=None
     
     start_length:float=0.9
     start_radius:float=0.1
     sections:int=5
     seed:int| None=None
     stochasticity:float=0.0
     branch_color:str="bark"
     
     leaves:bool=True
     leaf_length:float=0.35
     leaf_width:float=0.18
     leaf_fork_angle:float=40.0
     leaf_color:str="leaf"
     
@dataclass(frozen=True)
class Preset:
     iterations: int
     axiom: str
     rules: dict[str, Rule]
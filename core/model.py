from dataclasses import dataclass, field
from typing import List

@dataclass
class Restriction:
    coefficient: list[float]
    type: str
    rhs: float

@dataclass
class LPModel:
    sense: str
    objective_coefficient: list[float]
    variables: List[str]
    restrictions: List[Restriction] = field(default_factory=list)
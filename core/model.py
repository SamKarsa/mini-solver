from dataclasses import dataclass, field
from typing import List


@dataclass
class Restriction:
    coefficients: list[float]
    type: str
    rhs: float


@dataclass
class LPModel:
    sense: str
    objective_coefficients: list[float]
    variables: List[str]
    restrictions: List[Restriction] = field(default_factory=list)

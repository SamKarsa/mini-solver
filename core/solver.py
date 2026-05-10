from scipy.optimize import linprog
from dataclasses import dataclass
from core.model import LPModel


@dataclass
class SolverResult:
    status: str
    objective_value: float
    variables: dict
    restrictions: list


def solve(model: LPModel) -> SolverResult:
    # scipy siempre minimiza, si es maximizar invertimos los coeficientes
    coefficients = model.objective_coefficients
    if model.sense == 'max':
        coefficients = [-c for c in coefficients]

    A_ub, b_ub = [], []
    A_eq, b_eq = [], []

    for r in model.restrictions:
        if r.type == '<=':
            A_ub.append(r.coefficients)
            b_ub.append(r.rhs)
        elif r.type == '>=':
            # Multiplicamos por -1 para convertir >= en <=
            A_ub.append([-c for c in r.coefficients])
            b_ub.append(-r.rhs)
        elif r.type == '==':
            A_eq.append(r.coefficients)
            b_eq.append(r.rhs)

    # Ejecutar linprog
    result = linprog(
        c=coefficients,
        A_ub=A_ub if A_ub else None,
        b_ub=b_ub if b_ub else None,
        A_eq=A_eq if A_eq else None,
        b_eq=b_eq if b_eq else None,
        bounds=[(0, None)] * len(model.variables),
        method='highs'
    )

    return _interpret_result(result, model)


def _interpret_result(result, model: LPModel) -> SolverResult:
    # Mapear los codigos de scipy a mensajes legibles
    status_map = {
        0: "Solución óptima encontrada",
        1: "No se alcanzó la iteración límite",
        2: "Modelo no factible",
        3: "Modelo no acotado",
        4: "Error numérico",
    }

    status = status_map.get(result.status, "Estado desconocido")

    if result.status != 0:
        return SolverResult(
            status=status,
            objective_value=None,
            variables={},
            restrictions=[]
        )

    # Valor real de la función objetivo (re-invertir si era maximización)
    obj_value = -result.fun if model.sense == 'max' else result.fun

    # Valor de cada variable
    var_values = {
        name: round(val, 4)
        for name, val in zip(model.variables, result.x)
    }

    # Evaluación y holgura de cada restricción
    restriction_info = []
    for i, r in enumerate(model.restrictions):
        lhs = sum(c * result.x[j] for j, c in enumerate(r.coefficients))
        slack = r.rhs - lhs

        restriction_info.append({
            "restriction": f"R{i + 1}",
            "lhs": round(lhs, 4),
            "type": r.type,
            "rhs": r.rhs,
            "slack": round(slack, 4),
            "status": "Activa" if abs(slack) < 1e-6 else "Inactiva"
        })

    return SolverResult(
        status=status,
        objective_value=round(obj_value, 4),
        variables=var_values,
        restrictions=restriction_info
    )

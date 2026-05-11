import os
import json
from groq import Groq
from dotenv import load_dotenv
from core.model import LPModel, Restriction

load_dotenv()

_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Categorías de error que entiende la UI
ERR_API = "api"             # falló la llamada a la API (red, auth, rate limit)
ERR_PARSE = "parse"         # la IA devolvió algo que no es JSON válido
ERR_INTERPRET = "interpret" # la IA devolvió {"error": ...} (no pudo extraer modelo)
ERR_INVALID = "invalid"     # el modelo extraído tiene campos faltantes/inconsistentes

_SYSTEM_PROMPT = """
Eres un experto en programación lineal. Tu única tarea es extraer un modelo
de programación lineal a partir de un texto en lenguaje natural y devolverlo
en formato JSON.

Responde ÚNICAMENTE con un objeto JSON válido, sin texto adicional, sin
explicaciones, sin bloques de código markdown.

El JSON debe tener exactamente esta estructura:
{
  "sense": "max" o "min",
  "variables": ["x1", "x2", ...],
  "objective_coefficients": [c1, c2, ...],
  "restrictions": [
    {
      "coefficients": [a1, a2, ...],
      "type": "<=" o ">=" o "==",
      "rhs": b
    }
  ],
  "explanation": "Explicación breve de cómo interpretaste el problema"
}

Reglas:
- Cada variable debe tener su coeficiente en objective_coefficients en el mismo orden
- Cada restricción debe tener coeficientes para TODAS las variables en el mismo orden
- Si una variable no aparece en una restricción, su coeficiente es 0
- La no negatividad (xi >= 0) NO se incluye como restricción
- Si no puedes identificar un modelo lineal válido, devuelve: {"error": "mensaje explicando el problema"}
"""


def _err(kind: str, technical: str = "") -> dict:
    return {"error": True, "kind": kind, "technical": technical}


def _strip_code_fence(raw: str) -> str:
    """Algunos modelos meten el JSON dentro de ```json ... ``` aunque les
    digas que no. Removemos ese wrapping si aparece."""
    s = raw.strip()
    if s.startswith("```"):
        lines = s.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        s = "\n".join(lines).strip()
    return s


def parse_problem(text: str) -> dict:
    """Extrae un modelo de PL desde lenguaje natural.

    Devuelve:
      - {"model": LPModel, "explanation": str} en caso de éxito.
      - {"error": True, "kind": str, "technical": str} en caso de fallo.
    """
    # === 1) Llamada a la API ===
    try:
        response = _client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            temperature=0.1,
            max_tokens=1000,
        )
        raw = response.choices[0].message.content
        if not raw:
            return _err(ERR_API, "La API devolvió una respuesta vacía.")
        raw = raw.strip()
    except Exception as e:
        return _err(ERR_API, f"{type(e).__name__}: {e}")

    # === 2) Parseo del JSON ===
    cleaned = _strip_code_fence(raw)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        return _err(ERR_PARSE,
                    f"JSON inválido en posición {e.pos}: {e.msg}\n"
                    f"Respuesta cruda: {raw[:300]}")

    if not isinstance(data, dict):
        return _err(ERR_PARSE,
                    f"Se esperaba un objeto JSON, llegó {type(data).__name__}.")

    # === 3) La IA dijo explícitamente que no pudo ===
    if "error" in data and "sense" not in data:
        return _err(ERR_INTERPRET, str(data.get("error", "")))

    # === 4) Validación de estructura ===
    required = ["sense", "variables", "objective_coefficients", "restrictions"]
    missing = [k for k in required if k not in data]
    if missing:
        return _err(ERR_INVALID, f"Faltan campos en el JSON: {missing}")

    if data["sense"] not in ("max", "min"):
        return _err(ERR_INVALID, f"sense inválido: {data['sense']!r}")

    if not isinstance(data["variables"], list) or not data["variables"]:
        return _err(ERR_INVALID, "variables debe ser una lista no vacía.")

    if not isinstance(data["objective_coefficients"], list):
        return _err(ERR_INVALID, "objective_coefficients debe ser una lista.")

    n_vars = len(data["variables"])
    if len(data["objective_coefficients"]) != n_vars:
        return _err(ERR_INVALID,
                    f"Número de coeficientes ({len(data['objective_coefficients'])}) "
                    f"no coincide con número de variables ({n_vars}).")

    if not isinstance(data["restrictions"], list) or not data["restrictions"]:
        return _err(ERR_INVALID, "Debe haber al menos una restricción.")

    # === 5) Validación de cada restricción ===
    restrictions = []
    for i, r in enumerate(data["restrictions"], start=1):
        if not isinstance(r, dict):
            return _err(ERR_INVALID, f"Restricción {i} no es un objeto JSON.")
        for fld in ("coefficients", "type", "rhs"):
            if fld not in r:
                return _err(ERR_INVALID,
                            f"Restricción {i} no tiene el campo '{fld}'.")
        if not isinstance(r["coefficients"], list) or len(r["coefficients"]) != n_vars:
            return _err(ERR_INVALID,
                        f"Restricción {i}: cantidad de coeficientes "
                        f"({len(r['coefficients']) if isinstance(r['coefficients'], list) else '?'}) "
                        f"no coincide con número de variables ({n_vars}).")
        if r["type"] not in ("<=", ">=", "=="):
            return _err(ERR_INVALID,
                        f"Restricción {i}: tipo inválido {r['type']!r}.")
        try:
            restrictions.append(Restriction(
                coefficients=[float(c) for c in r["coefficients"]],
                type=r["type"],
                rhs=float(r["rhs"])
            ))
        except (ValueError, TypeError) as e:
            return _err(ERR_INVALID,
                        f"Restricción {i}: no pude convertir números: {e}")

    # === 6) Construcción del modelo ===
    try:
        model = LPModel(
            sense=data["sense"],
            objective_coefficients=[float(c) for c in data["objective_coefficients"]],
            variables=[str(v) for v in data["variables"]],
            restrictions=restrictions
        )
    except (ValueError, TypeError) as e:
        return _err(ERR_INVALID, f"Error construyendo el modelo: {e}")

    return {
        "model": model,
        "explanation": data.get("explanation", "")
    }

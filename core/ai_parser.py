import os
import json
from groq import Groq
from dotenv import load_dotenv
from core.model import LPModel, Restriction

load_dotenv()

_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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

def parse_problem(text: str) -> LPModel | dict:
    # Llama a Groq y parsea la respuesta como LPModel
    response = _client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        temperature=0.1,  # Baja temperatura para respuestas consistentes
        max_tokens=1000,
    )

    raw = response.choices[0].message.content.strip()

    # Parsear el JSON
    data = json.loads(raw)

    # Si la IA devolvió un error
    if "error" in data:
        return {"error": data["error"]}

    # Construir el LPModel
    restrictions = [
        Restriction(
            coefficients=r["coefficients"],
            type=r["type"],
            rhs=r["rhs"]
        )
        for r in data["restrictions"]
    ]

    model = LPModel(
        sense=data["sense"],
        objective_coefficients=data["objective_coefficients"],
        variables=data["variables"],
        restrictions=restrictions
    )

    # Retornar también la explicación para mostrarla en la UI
    return {
        "model": model,
        "explanation": data.get("explanation", "")
    }
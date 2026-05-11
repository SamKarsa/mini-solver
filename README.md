# LP Solver

Solver interactivo de programación lineal con dos modos de uso: entrada manual de coeficientes o descripción del problema en lenguaje natural (interpretada por IA).

![Python](https://img.shields.io/badge/python-3.12-blue) ![Streamlit](https://img.shields.io/badge/streamlit-1.57-red) ![HiGHS](https://img.shields.io/badge/solver-HiGHS-green)

---

## Features

- **Modo Manual** — tabla de coeficientes editable con scroll horizontal automático cuando hay muchas variables (hasta 20). Botones para agregar/quitar restricciones, selectores de tipo (≤, ≥, =), validación de inputs.
- **Modo IA** — describe el problema en lenguaje natural y la IA extrae variables, función objetivo y restricciones automáticamente (powered by Groq + Llama 3.3 70B).
- **Editar en Manual** — un click después de la interpretación de la IA carga el modelo extraído en la tabla manual para ajustar cualquier valor antes de re-resolver.
- **Resultados completos** — valor óptimo Z, valor de cada variable, holgura por restricción, identificación de cuellos de botella (restricciones activas vs inactivas).
- **Manejo de errores robusto** — la IA puede fallar de varias formas (red, JSON inválido, problema no interpretable). Cada caso se muestra con un mensaje accionable y un expander con el detalle técnico.

---

## Stack

| Capa | Tecnología |
|---|---|
| UI | [Streamlit](https://streamlit.io/) 1.57 |
| Solver | [scipy.optimize.linprog](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html) con backend [HiGHS](https://highs.dev/) |
| IA | [Groq API](https://groq.com/) — modelo `llama-3.3-70b-versatile` |
| Lenguaje | Python 3.12 |

---

## Instalación

```bash
# Clonar el repo
git clone https://github.com/<tu-usuario>/mini-solver.git
cd mini-solver

# Crear venv e instalar dependencias
python -m venv .venv
source .venv/bin/activate     # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Configuración

Para usar el **modo IA** necesitás una API key de Groq (gratis con cuenta en [console.groq.com](https://console.groq.com/)).

Crear un archivo `.env` en la raíz del proyecto:

```env
GROQ_API_KEY=tu_api_key_aqui
```

> El modo Manual funciona sin API key — solo necesitás Groq si querés usar la interpretación por lenguaje natural.

---

## Uso

```bash
streamlit run app.py
```

Abrir el navegador en la URL que muestre Streamlit (por defecto `http://localhost:8501`).

### Modo Manual

1. Configurá el número de variables (hasta 20) y el sentido (`max` / `min`).
2. Llená la tabla:
   - Fila **Z** (naranja): coeficientes de la función objetivo.
   - Filas **R1, R2, ...**: coeficientes de cada restricción, su tipo (≤, ≥, =) y el RHS.
3. Usá **+ restricción** / **− restricción** para ajustar el número de filas.
4. Presioná **Resolver**.

### Modo IA

1. Cambiá al modo **IA** con el selector arriba.
2. Describí el problema en lenguaje natural. Ejemplo:
   > Una fábrica produce sillas y mesas. Cada silla genera $3 de ganancia y toma 2 horas. Cada mesa genera $5 y toma 3 horas. Hay 12 horas disponibles y máximo 4 sillas. ¿Cuánto producir para maximizar la ganancia?
3. Presioná **Interpretar y Resolver**.
4. Revisá la interpretación de la IA y los resultados. Si algo está mal, usá **Editar en Manual →** para corregir en la tabla.

### Botón Limpiar

Resetea variables, coeficientes, descripción de la IA y resultados manteniendo el modo seleccionado.

---

## Estructura del proyecto

```
mini-solver/
├── app.py                  # Entry point: selector de modo, layout principal
├── core/
│   ├── model.py            # Dataclasses: LPModel, Restriction
│   ├── solver.py           # Wrapper de scipy.linprog (max→min, ≥→≤, holgura)
│   └── ai_parser.py        # Cliente de Groq + validación del modelo extraído
├── ui/
│   └── components.py       # Estilos CSS y todos los componentes de UI
└── requirements.txt
```

---

## Cómo leer los resultados

- **Valor óptimo Z**: mejor resultado de la función objetivo que cumple todas las restricciones.
- **Variables**: valor de cada xᵢ en el óptimo.
- **Holgura**: `RHS − LHS` de cada restricción.
  - Si ≈ 0 → restricción **Activa** (cuello de botella, está al límite).
  - Si > 0 → restricción **Inactiva** (recurso sobrante).

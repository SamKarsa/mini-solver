# ui/componentes.py
import streamlit as st
from core.model import LPModel, Restriction


_FONTS_URL = "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Syne:wght@400;600;800&display=swap"  # noqa: E501


def apply_styles():
    st.markdown("""
        <style>
            @import url('""" + _FONTS_URL + """');

            /* Base */
            html, body, [class*="css"] {
                font-family: 'Syne', sans-serif;
                background-color: #0f1117;
                color: #e0e0e0;
            }

            /* Ocultar header de streamlit */
            header { visibility: hidden; }

            /* Título principal */
            .main-title {
                font-family: 'Syne', sans-serif;
                font-weight: 800;
                font-size: 2.2rem;
                color: #ffffff;
                letter-spacing: -0.5px;
            }

            .accent { color: #00ff88; }

            .subtitle {
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.75rem;
                color: #555;
                margin-top: -10px;
                margin-bottom: 30px;
            }

            /* Tarjetas de sección */
            .section-card {
                background: #1a1d27;
                border: 1px solid #2a2d3a;
                border-radius: 12px;
                padding: 24px;
                margin-bottom: 16px;
            }

            .section-title {
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.7rem;
                color: #00ff88;
                letter-spacing: 2px;
                text-transform: uppercase;
                margin-bottom: 16px;
            }

            /* Inputs */
            .stNumberInput input, .stTextInput input, .stSelectbox select {
                background: #0f1117 !important;
                border: 1px solid #2a2d3a !important;
                border-radius: 8px !important;
                color: #e0e0e0 !important;
                font-family: 'JetBrains Mono', monospace !important;
            }

            /* Botón resolver */
            .stButton > button {
                background: #00ff88 !important;
                color: #0f1117 !important;
                font-family: 'Syne', sans-serif !important;
                font-weight: 600 !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 12px 32px !important;
                font-size: 1rem !important;
                width: 100% !important;
                transition: opacity 0.2s !important;
            }

            .stButton > button:hover {
                opacity: 0.85 !important;
            }

            /* Resultado óptimo */
            .result-value {
                font-family: 'JetBrains Mono', monospace;
                font-size: 2.5rem;
                font-weight: 600;
                color: #00ff88;
            }

            .result-label {
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.7rem;
                color: #555;
                text-transform: uppercase;
                letter-spacing: 2px;
            }

            /* Badge de estado */
            .badge-optimal {
                display: inline-block;
                background: rgba(0, 255, 136, 0.1);
                color: #00ff88;
                border: 1px solid rgba(0, 255, 136, 0.3);
                border-radius: 20px;
                padding: 4px 14px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.75rem;
            }

            .badge-error {
                display: inline-block;
                background: rgba(255, 80, 80, 0.1);
                color: #ff5050;
                border: 1px solid rgba(255, 80, 80, 0.3);
                border-radius: 20px;
                padding: 4px 14px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.75rem;
            }

            /* Variables resultado */
            .var-row {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px 0;
                border-bottom: 1px solid #2a2d3a;
                font-family: 'JetBrains Mono', monospace;
            }

            .var-name { color: #888; font-size: 0.85rem; }
            .var-val  { color: #ffffff; font-size: 0.95rem; font-weight: 600; }

            /* Tabla restricciones */
            .rest-row {
                display: grid;
                grid-template-columns: 60px 1fr 60px 80px 80px;
                gap: 8px;
                padding: 10px 0;
                border-bottom: 1px solid #2a2d3a;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.8rem;
                align-items: center;
            }

            .rest-header {
                color: #555;
                font-size: 0.65rem;
                text-transform: uppercase;
                letter-spacing: 1px;
            }

            .tag-active {
                background: rgba(0, 255, 136, 0.1);
                color: #00ff88;
                border-radius: 4px;
                padding: 2px 8px;
                font-size: 0.7rem;
            }

            .tag-inactive {
                background: rgba(255, 255, 255, 0.05);
                color: #666;
                border-radius: 4px;
                padding: 2px 8px;
                font-size: 0.7rem;
            }

            /* Divider */
            hr { border-color: #2a2d3a !important; }
        </style>
    """, unsafe_allow_html=True)


def render_header():
    # Encabezado principal
    st.markdown("""
        <div class="main-title">LP <span class="accent">Solver</span></div>
        <div class="subtitle">// linear programming optimizer</div>
    """, unsafe_allow_html=True)


def render_model_input():
    # Sección de configuración del modelo — retorna el modelo construido o None
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">// Configuración</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        n_vars = st.number_input("Número de variables", min_value=1, max_value=10, value=2, step=1)
    with col2:
        sense = st.selectbox("Sentido", ["max", "min"])

    # Nombres de variables
    var_names = []
    st.markdown("**Variables**")
    cols = st.columns(n_vars)
    for i, col in enumerate(cols):
        with col:
            name = st.text_input(f"Var {i+1}", value=f"x{i+1}", key=f"var_name_{i}")
            var_names.append(name)

    st.markdown('</div>', unsafe_allow_html=True)

    # Función objetivo
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">// Función Objetivo</div>', unsafe_allow_html=True)

    obj_coeffs = []
    cols = st.columns(n_vars)
    for i, col in enumerate(cols):
        with col:
            c = st.number_input(f"{var_names[i]}", value=1.0, key=f"obj_{i}", format="%.2f")
            obj_coeffs.append(c)

    st.markdown('</div>', unsafe_allow_html=True)

    # Restricciones
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">// Restricciones</div>', unsafe_allow_html=True)

    if "n_restrictions" not in st.session_state:
        st.session_state.n_restrictions = 2

    restrictions = []
    for r in range(st.session_state.n_restrictions):
        st.markdown(f"**R{r+1}**")
        cols = st.columns(n_vars + 2)

        coeffs = []
        for i in range(n_vars):
            with cols[i]:
                c = st.number_input(var_names[i], value=1.0, key=f"r{r}_c{i}", format="%.2f")
                coeffs.append(c)

        with cols[n_vars]:
            r_type = st.selectbox("", ["<=", ">=", "=="], key=f"r{r}_type")

        with cols[n_vars + 1]:
            rhs = st.number_input("RHS", value=10.0, key=f"r{r}_rhs", format="%.2f")

        restrictions.append(Restriction(coefficients=coeffs, type=r_type, rhs=rhs))

    col1, col2 = st.columns(2)
    with col1:
        if st.button("+ Restricción"):
            st.session_state.n_restrictions += 1
            st.rerun()
    with col2:
        if st.button("- Restricción") and st.session_state.n_restrictions > 1:
            st.session_state.n_restrictions -= 1
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    return LPModel(
        sense=sense,
        objective_coefficients=obj_coeffs,
        variables=var_names,
        restrictions=restrictions
    )


def render_results(result):
    # Panel de resultados
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">// Resultados</div>', unsafe_allow_html=True)

    # Badge de estado
    is_optimal = result.status == "Solución óptima encontrada"
    badge_class = "badge-optimal" if is_optimal else "badge-error"
    st.markdown(f'<span class="{badge_class}">{result.status}</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if not is_optimal:
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Valor óptimo
    st.markdown(f"""
        <div class="result-label">Valor óptimo</div>
        <div class="result-value">Z = {result.objective_value}</div>
        <br>
    """, unsafe_allow_html=True)

    # Variables
    st.markdown('<div class="section-title">// Variables</div>', unsafe_allow_html=True)
    for name, val in result.variables.items():
        st.markdown(f"""
            <div class="var-row">
                <span class="var-name">{name}</span>
                <span class="var-val">{val}</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Restricciones
    st.markdown('<div class="section-title">// Restricciones</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="rest-row">
            <span class="rest-header">ID</span>
            <span class="rest-header">LHS</span>
            <span class="rest-header">RHS</span>
            <span class="rest-header">Holgura</span>
            <span class="rest-header">Estado</span>
        </div>
    """, unsafe_allow_html=True)

    for r in result.restrictions:
        tag_class = "tag-active" if r["status"] == "Activa" else "tag-inactive"
        st.markdown(f"""
            <div class="rest-row">
                <span style="color:#888">{r['restriction']}</span>
                <span>{r['lhs']}</span>
                <span>{r['rhs']}</span>
                <span>{r['slack']}</span>
                <span class="{tag_class}">{r['status']}</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

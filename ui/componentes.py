# ui/componentes.py
from textwrap import dedent

import streamlit as st
from core.model import LPModel, Restriction


_FONTS_URL = "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Syne:wght@400;600;700;800&display=swap"  # noqa: E501


def apply_styles():
    st.markdown("""
        <style>
            @import url('""" + _FONTS_URL + """');

            /* === Base === */
            .stApp, [data-testid="stAppViewContainer"] {
                background:
                    radial-gradient(circle at 15% -10%, rgba(0,255,136,0.08), transparent 40%),
                    radial-gradient(circle at 90% 110%, rgba(0,255,136,0.05), transparent 40%),
                    #0a0c12;
                font-family: 'Syne', sans-serif;
                color: #e0e0e0;
            }
            [data-testid="stHeader"] { display: none; }
            [data-testid="stToolbar"] { display: none; }
            .block-container { padding-top: 2rem !important; max-width: 1400px; }

            /* === Bordered containers (cards) === */
            [data-testid="stVerticalBlockBorderWrapper"] {
                background: linear-gradient(180deg, #14171f 0%, #11141b 100%);
                border: 1px solid #1f2330 !important;
                border-radius: 14px;
                padding: 22px 24px !important;
                margin-bottom: 14px;
                transition: border-color 0.2s;
            }
            [data-testid="stVerticalBlockBorderWrapper"]:hover {
                border-color: #2a3040 !important;
            }

            /* === Hero === */
            .hero-wrap {
                display: flex;
                justify-content: space-between;
                align-items: flex-end;
                margin-bottom: 28px;
                padding-bottom: 18px;
                border-bottom: 1px solid #1f2330;
            }
            .hero-title {
                font-family: 'Syne', sans-serif;
                font-weight: 800;
                font-size: 3.6rem;
                color: #ffffff;
                line-height: 0.95;
                letter-spacing: -2.5px;
            }
            .hero-title .accent {
                background: linear-gradient(135deg, #00ff88 0%, #00d4aa 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            .hero-sub {
                font-family: 'JetBrains Mono', monospace;
                color: #4a5060;
                font-size: 0.78rem;
                margin-top: 10px;
                letter-spacing: 0.5px;
            }
            .status-dot {
                display: inline-block;
                width: 7px; height: 7px;
                background: #00ff88;
                border-radius: 50%;
                margin-right: 8px;
                box-shadow: 0 0 10px #00ff88;
                animation: pulse 2s ease-in-out infinite;
            }
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            .hero-meta {
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.7rem;
                color: #4a5060;
                text-align: right;
                letter-spacing: 1px;
            }
            .hero-meta .label { color: #2a3040; }

            /* === Section titles === */
            .section-title {
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.68rem;
                color: #00ff88;
                letter-spacing: 2.5px;
                text-transform: uppercase;
                margin-bottom: 18px;
                font-weight: 600;
            }

            /* === Labels above inputs === */
            label, .stMarkdown p strong {
                font-family: 'JetBrains Mono', monospace !important;
                font-size: 0.72rem !important;
                color: #6a7080 !important;
                letter-spacing: 0.5px !important;
                text-transform: lowercase !important;
            }

            /* === Inputs === */
            .stNumberInput input,
            .stTextInput input {
                background: #0a0c12 !important;
                border: 1px solid #1f2330 !important;
                border-radius: 8px !important;
                color: #ffffff !important;
                font-family: 'JetBrains Mono', monospace !important;
                font-weight: 500 !important;
                transition: border-color 0.2s, box-shadow 0.2s;
            }
            .stNumberInput input:focus,
            .stTextInput input:focus {
                border-color: #00ff88 !important;
                box-shadow: 0 0 0 3px rgba(0,255,136,0.1) !important;
            }
            .stSelectbox > div > div {
                background: #0a0c12 !important;
                border: 1px solid #1f2330 !important;
                border-radius: 8px !important;
                color: #ffffff !important;
                font-family: 'JetBrains Mono', monospace !important;
            }

            /* === Number input +/- buttons === */
            .stNumberInput button {
                background: #14171f !important;
                border: 1px solid #1f2330 !important;
                color: #6a7080 !important;
            }
            .stNumberInput button:hover {
                background: #1f2330 !important;
                color: #00ff88 !important;
            }

            /* === Primary button === */
            .stButton > button {
                background: linear-gradient(135deg, #00ff88 0%, #00d4aa 100%) !important;
                color: #0a0c12 !important;
                font-family: 'Syne', sans-serif !important;
                font-weight: 700 !important;
                border: none !important;
                border-radius: 10px !important;
                padding: 14px 32px !important;
                font-size: 0.95rem !important;
                width: 100% !important;
                letter-spacing: 0.5px !important;
                transition: transform 0.15s, box-shadow 0.15s !important;
                box-shadow: 0 0 0 rgba(0,255,136,0);
            }
            .stButton > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 6px 20px rgba(0,255,136,0.25) !important;
            }

            /* === Secondary buttons (+/- restricción) === */
            .stButton > button[kind="secondary"] {
                background: #14171f !important;
                color: #6a7080 !important;
                font-weight: 500 !important;
                border: 1px solid #1f2330 !important;
                box-shadow: none !important;
            }

            /* === Result display === */
            .result-label {
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.65rem;
                color: #4a5060;
                text-transform: uppercase;
                letter-spacing: 2.5px;
                margin-bottom: 6px;
            }
            .result-value {
                font-family: 'Syne', sans-serif;
                font-size: 3rem;
                font-weight: 800;
                background: linear-gradient(135deg, #00ff88 0%, #00d4aa 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                letter-spacing: -1px;
                line-height: 1;
            }

            /* === Status badges === */
            .badge {
                display: inline-block;
                border-radius: 20px;
                padding: 5px 14px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.72rem;
                font-weight: 500;
                letter-spacing: 0.3px;
            }
            .badge-optimal {
                background: rgba(0, 255, 136, 0.08);
                color: #00ff88;
                border: 1px solid rgba(0, 255, 136, 0.25);
            }
            .badge-error {
                background: rgba(255, 80, 80, 0.08);
                color: #ff5050;
                border: 1px solid rgba(255, 80, 80, 0.25);
            }

            /* === Variables list === */
            .var-row {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px 14px;
                margin-bottom: 6px;
                background: #0a0c12;
                border: 1px solid #1f2330;
                border-radius: 8px;
                font-family: 'JetBrains Mono', monospace;
            }
            .var-name { color: #6a7080; font-size: 0.85rem; }
            .var-val  { color: #00ff88; font-size: 1rem; font-weight: 600; }

            /* === Restrictions table === */
            .rest-row {
                display: grid;
                grid-template-columns: 50px 1fr 1fr 1fr 90px;
                gap: 12px;
                padding: 11px 14px;
                margin-bottom: 4px;
                background: #0a0c12;
                border: 1px solid #1f2330;
                border-radius: 8px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.82rem;
                align-items: center;
                color: #c0c5d1;
            }
            .rest-header-row {
                background: transparent;
                border: none;
                padding: 6px 14px;
                margin-bottom: 4px;
            }
            .rest-header {
                color: #4a5060;
                font-size: 0.62rem;
                text-transform: uppercase;
                letter-spacing: 1.5px;
            }
            .tag-active {
                background: rgba(0, 255, 136, 0.1);
                color: #00ff88;
                border-radius: 5px;
                padding: 3px 9px;
                font-size: 0.68rem;
                text-align: center;
                font-weight: 500;
            }
            .tag-inactive {
                background: rgba(120, 130, 150, 0.08);
                color: #6a7080;
                border-radius: 5px;
                padding: 3px 9px;
                font-size: 0.68rem;
                text-align: center;
                font-weight: 500;
            }

            /* === Empty state === */
            .empty-state {
                min-height: 380px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                gap: 10px;
                color: #4a5060;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.82rem;
                text-align: center;
            }
            .empty-icon {
                font-size: 2.8rem;
                opacity: 0.15;
                margin-bottom: 4px;
            }
            .empty-hint {
                font-size: 0.7rem;
                color: #2a3040;
                letter-spacing: 0.5px;
            }

            /* === Restriction row labels === */
            .r-label {
                font-family: 'JetBrains Mono', monospace;
                font-weight: 600;
                color: #00ff88;
                font-size: 0.85rem;
                margin-top: 14px;
                margin-bottom: 6px;
                letter-spacing: 1px;
            }

            /* === Expander (help section) === */
            [data-testid="stExpander"] {
                border: 1px solid #1f2330 !important;
                border-radius: 12px !important;
                background: linear-gradient(180deg, #14171f 0%, #11141b 100%) !important;
                margin-bottom: 22px;
            }
            [data-testid="stExpander"] summary {
                font-family: 'JetBrains Mono', monospace !important;
                color: #00ff88 !important;
                font-size: 0.78rem !important;
                letter-spacing: 1.5px !important;
                text-transform: uppercase !important;
                padding: 14px 20px !important;
            }
            [data-testid="stExpander"] summary:hover {
                color: #00d4aa !important;
            }
            [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
                padding: 0 22px 20px 22px !important;
            }

            /* === Code blocks in help === */
            .stCode, [data-testid="stCode"] {
                background: #0a0c12 !important;
                border: 1px solid #1f2330 !important;
                border-radius: 8px !important;
            }
            code {
                color: #00ff88 !important;
                font-family: 'JetBrains Mono', monospace !important;
            }

            /* === Help section text === */
            .help-content {
                color: #c0c5d1;
                font-family: 'Syne', sans-serif;
                line-height: 1.6;
                font-size: 0.92rem;
            }
            .help-content h3 {
                font-family: 'JetBrains Mono', monospace;
                color: #00ff88;
                font-size: 0.72rem;
                letter-spacing: 2px;
                text-transform: uppercase;
                margin-top: 22px;
                margin-bottom: 12px;
                font-weight: 600;
            }
            .help-content strong { color: #ffffff; }
            .step-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 12px;
                margin-top: 12px;
            }
            .step-card {
                background: #0a0c12;
                border: 1px solid #1f2330;
                border-radius: 10px;
                padding: 14px 16px;
            }
            .step-num {
                font-family: 'JetBrains Mono', monospace;
                color: #00ff88;
                font-size: 0.7rem;
                letter-spacing: 1.5px;
                margin-bottom: 6px;
            }
            .step-text {
                color: #c0c5d1;
                font-size: 0.86rem;
                line-height: 1.5;
            }
            .lp-block {
                background: #0a0c12;
                border: 1px solid #1f2330;
                border-left: 3px solid #00ff88;
                border-radius: 8px;
                padding: 14px 18px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.82rem;
                color: #c0c5d1;
                white-space: pre;
                line-height: 1.7;
                margin: 10px 0;
                overflow-x: auto;
            }

            hr { border-color: #1f2330 !important; }
        </style>
    """, unsafe_allow_html=True)


def render_header():
    st.markdown("""
        <div class="hero-wrap">
            <div>
                <div class="hero-title">LP <span class="accent">Solver</span></div>
                <div class="hero-sub">
                    <span class="status-dot"></span>linear programming optimizer · powered by HiGHS
                </div>
            </div>
            <div class="hero-meta">
                <span class="label">// version</span> 1.0.0<br>
                <span class="label">// engine</span> simplex / interior-point
            </div>
        </div>
    """, unsafe_allow_html=True)


_HELP_HTML = dedent("""
    <div class="help-content">
    <h3>// ¿Qué es la Programación Lineal?</h3>
    <p>La <strong>Programación Lineal (PL)</strong> es una técnica de
    optimización matemática para encontrar el mejor resultado (máximo o
    mínimo) de una función lineal, dadas ciertas restricciones también
    lineales. Se usa en asignación de recursos, planificación de producción,
    dietas, rutas de transporte, mezcla de materiales, etc.</p>

    <h3>// Forma estándar</h3>
    <div class="lp-block">max/min  Z = c₁·x₁ + c₂·x₂ + ... + cₙ·xₙ
    sujeto a:
        a₁₁·x₁ + a₁₂·x₂ + ... ≤ b₁
        a₂₁·x₁ + a₂₂·x₂ + ... ≥ b₂
        a₃₁·x₁ + a₃₂·x₂ + ... = b₃
        xᵢ ≥ 0   (no negatividad)</div>

    <h3>// Pasos para usarlo</h3>
    <div class="step-grid">
      <div class="step-card">
        <div class="step-num">// 01 · CONFIGURACIÓN</div>
        <div class="step-text">Elige <strong>max</strong> o <strong>min</strong>,
        el número de variables, y nómbralas (x1, x2, ...).</div>
      </div>
      <div class="step-card">
        <div class="step-num">// 02 · OBJETIVO</div>
        <div class="step-text">Escribe los coeficientes <strong>cᵢ</strong>
        de cada variable en la función Z.</div>
      </div>
      <div class="step-card">
        <div class="step-num">// 03 · RESTRICCIONES</div>
        <div class="step-text">Por cada restricción, los coeficientes,
        el operador (≤, ≥, =), y el lado derecho <strong>b</strong>.</div>
      </div>
      <div class="step-card">
        <div class="step-num">// 04 · RESOLVER</div>
        <div class="step-text">Click en <strong>⚡ Resolver</strong>.
        Obtén Z*, los valores de cada xᵢ, y la holgura de cada restricción.</div>
      </div>
    </div>

    <h3>// Ejemplo · Problema de la fábrica</h3>
    <p>Una fábrica produce dos productos <strong>x₁</strong> y
    <strong>x₂</strong>. Cada uno deja una ganancia distinta y consume
    distintos recursos. Queremos maximizar la ganancia total respetando
    la capacidad de cada recurso.</p>

    <div class="lp-block">max  Z = 3·x₁ + 5·x₂

    s.a.
           x₁          ≤  4     (recurso A)
                  2·x₂ ≤ 12     (recurso B)
        3·x₁ +   2·x₂  ≤ 18     (recurso C)
        x₁, x₂ ≥ 0</div>

    <p>👉 <strong>Solución óptima:</strong>
    x₁ = 2, x₂ = 6, <strong>Z* = 36</strong></p>

    <h3>// Interpretando los resultados</h3>
    <p><strong>Z*</strong> es el valor óptimo de la función objetivo.<br>
    Cada <strong>xᵢ</strong> es la cantidad óptima de cada variable.<br>
    La <strong>holgura</strong> de una restricción es
    <code>b − (lado izquierdo)</code>: cuánto sobra/falta en ella.</p>

    <ul>
      <li><strong style="color:#00ff88">Activa</strong> (holgura ≈ 0):
      la restricción se cumple con igualdad — es un
      <em>cuello de botella</em>. Si pudieras relajarla, mejorarías Z.</li>
      <li><strong style="color:#6a7080">Inactiva</strong> (holgura &gt; 0):
      tienes margen sobrante. No es limitante.</li>
    </ul>
    </div>
""").strip()


def render_help():
    with st.expander("// ¿Cómo usar este solver?", expanded=False):
        st.markdown(_HELP_HTML, unsafe_allow_html=True)


def render_model_input():
    # === Sección · Configuración ===
    with st.container(border=True):
        st.markdown('<div class="section-title">// 01 · Configuración</div>',
                    unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])
        with col1:
            n_vars = st.number_input("Número de variables", min_value=1,
                                     max_value=10, value=2, step=1)
        with col2:
            sense = st.selectbox("Sentido", ["max", "min"])

        st.markdown('<div style="margin-top:8px"></div>', unsafe_allow_html=True)
        st.markdown("**Variables**")
        var_names = []
        cols = st.columns(n_vars)
        for i, col in enumerate(cols):
            with col:
                name = st.text_input(f"Var {i+1}", value=f"x{i+1}",
                                     key=f"var_name_{i}",
                                     label_visibility="collapsed")
                var_names.append(name)

    # === Sección · Función Objetivo ===
    with st.container(border=True):
        st.markdown('<div class="section-title">// 02 · Función Objetivo</div>',
                    unsafe_allow_html=True)

        obj_coeffs = []
        cols = st.columns(n_vars)
        for i, col in enumerate(cols):
            with col:
                c = st.number_input(f"{var_names[i]}", value=1.0,
                                    key=f"obj_{i}", format="%.2f")
                obj_coeffs.append(c)

    # === Sección · Restricciones ===
    with st.container(border=True):
        st.markdown('<div class="section-title">// 03 · Restricciones</div>',
                    unsafe_allow_html=True)

        if "n_restrictions" not in st.session_state:
            st.session_state.n_restrictions = 2

        restrictions = []
        for r in range(st.session_state.n_restrictions):
            st.markdown(f'<div class="r-label">// R{r+1}</div>',
                        unsafe_allow_html=True)
            cols = st.columns(n_vars + 2)

            coeffs = []
            for i in range(n_vars):
                with cols[i]:
                    c = st.number_input(var_names[i], value=1.0,
                                        key=f"r{r}_c{i}", format="%.2f")
                    coeffs.append(c)

            with cols[n_vars]:
                r_type = st.selectbox("Tipo", ["<=", ">=", "=="],
                                      key=f"r{r}_type",
                                      label_visibility="collapsed")

            with cols[n_vars + 1]:
                rhs = st.number_input("RHS", value=10.0, key=f"r{r}_rhs",
                                      format="%.2f")

            restrictions.append(Restriction(coefficients=coeffs,
                                            type=r_type, rhs=rhs))

        st.markdown('<div style="margin-top:8px"></div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("+ agregar", key="add_r", type="secondary"):
                st.session_state.n_restrictions += 1
                st.rerun()
        with col2:
            if st.button("− quitar", key="rm_r", type="secondary") \
                    and st.session_state.n_restrictions > 1:
                st.session_state.n_restrictions -= 1
                st.rerun()

    return LPModel(
        sense=sense,
        objective_coefficients=obj_coeffs,
        variables=var_names,
        restrictions=restrictions
    )


def render_empty_results():
    with st.container(border=True):
        st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">⊕</div>
                <div>// los resultados aparecerán aquí</div>
                <div class="empty-hint">configura tu modelo · presiona resolver</div>
            </div>
        """, unsafe_allow_html=True)


def render_results(result):
    is_optimal = result.status == "Solución óptima encontrada"
    badge_class = "badge-optimal" if is_optimal else "badge-error"

    # === Estado + valor óptimo ===
    with st.container(border=True):
        st.markdown('<div class="section-title">// Resultados</div>',
                    unsafe_allow_html=True)
        st.markdown(f'<span class="badge {badge_class}">{result.status}</span>',
                    unsafe_allow_html=True)

        if is_optimal:
            st.markdown(f"""
                <div style="margin-top: 22px;">
                    <div class="result-label">// valor óptimo</div>
                    <div class="result-value">Z = {result.objective_value}</div>
                </div>
            """, unsafe_allow_html=True)

    if not is_optimal:
        return

    # === Variables ===
    with st.container(border=True):
        st.markdown('<div class="section-title">// Variables</div>',
                    unsafe_allow_html=True)
        for name, val in result.variables.items():
            st.markdown(f"""
                <div class="var-row">
                    <span class="var-name">{name}</span>
                    <span class="var-val">{val}</span>
                </div>
            """, unsafe_allow_html=True)

    # === Restricciones ===
    with st.container(border=True):
        st.markdown('<div class="section-title">// Restricciones</div>',
                    unsafe_allow_html=True)
        st.markdown("""
            <div class="rest-row rest-header-row">
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
                    <span style="color:#6a7080">{r['restriction']}</span>
                    <span>{r['lhs']}</span>
                    <span>{r['rhs']}</span>
                    <span>{r['slack']}</span>
                    <span class="{tag_class}">{r['status']}</span>
                </div>
            """, unsafe_allow_html=True)

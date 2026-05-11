# ui/components.py
import streamlit as st
from core.model import LPModel, Restriction


def clear_session_keep_mode():
    """Limpia todo el session_state excepto la selección de modo (Manual/IA).
    Bumpea un contador para el textarea de IA — algunos widgets de texto
    de Streamlit no se rehidratan aunque su key se borre del session_state,
    así que al cambiar la key se fuerza un mount nuevo y queda vacío."""
    mode = st.session_state.get("mode", "Manual")
    ai_textarea_version = st.session_state.get("ai_textarea_version", 0) + 1
    for k in list(st.session_state.keys()):
        if k != "mode":
            del st.session_state[k]
    st.session_state.ai_textarea_version = ai_textarea_version


_FONTS_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=DM+Serif+Display&"
    "family=DM+Sans:wght@400;500;600&"
    "family=JetBrains+Mono:wght@400;500;600&"
    "display=swap"
)

# Paleta de colores
C = {
    "bg":       "#f5f4f0",   # Fondo general (crema)
    "surface":  "#fafaf8",   # Tarjetas
    "surface2": "#f0f0ec",   # Filas alternas, badges
    "input":    "#ffffff",   # Fondo de inputs (blanco para contraste)
    "inputBorder": "#cac9c3", # Borde de inputs (visible)
    "border":   "#e8e8e4",   # Bordes suaves
    "border2":  "#d4d3ce",   # Bordes énfasis
    "text":     "#1a1a1a",   # Texto principal
    "text2":    "#6b7280",   # Texto secundario
    "text3":    "#9ca3af",   # Hints
    "indigo":   "#4338ca",   # Acento principal
    "indigo2":  "#6366f1",   # Acento hover
    "orange":   "#ff6b35",   # Función objetivo
    "green":    "#16a34a",   # Éxito
    "red":      "#dc2626",   # Error
}


def apply_styles():
    st.markdown(f"""
        <style>
            @import url('{_FONTS_URL}');

            /* === Base === */
            .stApp, [data-testid="stAppViewContainer"] {{
                background: {C['bg']};
                font-family: 'DM Sans', sans-serif;
                color: {C['text']};
            }}
            [data-testid="stHeader"], [data-testid="stToolbar"] {{ display: none; }}
            .block-container {{
                padding-top: 2.5rem !important;
                max-width: 1500px !important;
            }}

            /* === Contenedores con borde === */
            [data-testid="stVerticalBlockBorderWrapper"] {{
                background: {C['surface']};
                border: 1px solid {C['border']} !important;
                border-radius: 12px;
                padding: 24px 28px !important;
                margin-bottom: 16px;
            }}

            /* === Títulos de sección === */
            .section-title {{
                font-family: 'DM Sans', sans-serif;
                font-size: 0.7rem;
                font-weight: 600;
                color: {C['indigo']};
                letter-spacing: 2px;
                text-transform: uppercase;
                margin-bottom: 18px;
            }}

            /* === Labels === */
            label, .stMarkdown p {{
                font-family: 'DM Sans', sans-serif !important;
                font-size: 0.8rem !important;
                color: {C['text2']} !important;
            }}

            /* === Inputs === */
            .stNumberInput input,
            .stTextInput input {{
                background: {C['input']} !important;
                border: 1px solid {C['inputBorder']} !important;
                border-radius: 8px !important;
                color: {C['text']} !important;
                font-family: 'JetBrains Mono', monospace !important;
                font-size: 0.9rem !important;
                font-weight: 500 !important;
                box-shadow: 0 1px 2px rgba(20, 20, 20, 0.04) !important;
                transition: border-color 0.15s, box-shadow 0.15s !important;
            }}
            .stNumberInput input:hover,
            .stTextInput input:hover {{
                border-color: {C['border2']} !important;
            }}
            .stNumberInput input:focus,
            .stTextInput input:focus {{
                border-color: {C['indigo']} !important;
                box-shadow: 0 0 0 3px rgba(67,56,202,0.15), 0 1px 2px rgba(20, 20, 20, 0.04) !important;
                outline: none !important;
            }}

            /* === Ocultar botones +/- de number_input === */
            .stNumberInput button {{
                display: none !important;
            }}

            /* === Excepción: mostrar botones solo en n_vars === */
            .st-key-n_vars .stNumberInput button {{
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                background: {C['surface2']} !important;
                border: 1px solid {C['border']} !important;
                color: {C['text2']} !important;
                border-radius: 6px !important;
                width: 36px !important;
                min-width: 36px !important;
            }}
            .st-key-n_vars .stNumberInput button:hover {{
                background: {C['border']} !important;
                color: {C['text']} !important;
                border-color: {C['indigo']} !important;
            }}

            /* === Radio selector de modo: pills con círculo === */
            .stRadio > div[role="radiogroup"] {{
                gap: 10px !important;
                background: transparent !important;
                padding: 0 !important;
            }}
            .stRadio [role="radiogroup"] > label {{
                background: {C['surface2']} !important;
                border: 1px solid {C['border']} !important;
                border-radius: 999px !important;
                padding: 7px 18px 7px 12px !important;
                cursor: pointer !important;
                margin: 0 !important;
                display: inline-flex !important;
                align-items: center !important;
                gap: 6px !important;
                transition: all 0.15s ease !important;
            }}
            .stRadio [role="radiogroup"] > label:hover {{
                border-color: {C['border2']} !important;
                background: {C['input']} !important;
            }}
            .stRadio [role="radiogroup"] > label p {{
                font-family: 'DM Sans', sans-serif !important;
                font-size: 0.88rem !important;
                font-weight: 500 !important;
                color: {C['text2']} !important;
                margin: 0 !important;
            }}
            /* Opción seleccionada: borde y texto índigo */
            .stRadio [role="radiogroup"] > label:has(input:checked) {{
                background: {C['input']} !important;
                border-color: {C['indigo']} !important;
                box-shadow: 0 0 0 3px rgba(67, 56, 202, 0.10) !important;
            }}
            .stRadio [role="radiogroup"] > label:has(input:checked) p {{
                color: {C['indigo']} !important;
                font-weight: 600 !important;
            }}
            /* El círculo visual del radio (BaseWeb) */
            .stRadio [role="radiogroup"] > label > div:first-child {{
                background: transparent !important;
            }}

            /* === Selectbox === */
            .stSelectbox > div > div {{
                background: {C['input']} !important;
                border: 1px solid {C['inputBorder']} !important;
                border-radius: 8px !important;
                color: {C['text']} !important;
                font-family: 'JetBrains Mono', monospace !important;
                font-size: 0.88rem !important;
                box-shadow: 0 1px 2px rgba(20, 20, 20, 0.04) !important;
                transition: border-color 0.15s !important;
            }}
            .stSelectbox > div > div:hover {{
                border-color: {C['border2']} !important;
            }}

            /* === Botón resolver (primario) === */
            .stButton > button[kind="primary"],
            .stButton > button {{
                background: {C['indigo']} !important;
                color: #ffffff !important;
                font-family: 'DM Sans', sans-serif !important;
                font-weight: 600 !important;
                border: none !important;
                border-radius: 10px !important;
                padding: 14px 32px !important;
                font-size: 0.95rem !important;
                width: 100% !important;
                letter-spacing: 0.3px !important;
                transition: background 0.15s !important;
            }}
            .stButton > button:hover {{
                background: {C['indigo2']} !important;
            }}

            /* === Resolver: ancho contenido, flush a la izquierda === */
            [data-testid="stElementContainer"]:has(> .stButton > button[kind="primary"]) {{
                padding: 0 !important;
                margin: 0 !important;
            }}
            .stButton:has(> button[kind="primary"]) {{
                display: block !important;
                width: 100% !important;
                padding: 0 !important;
                margin: 0 !important;
                text-align: left !important;
            }}
            .stButton > button[kind="primary"] {{
                width: 360px !important;
                max-width: 90% !important;
                display: block !important;
                margin: 0 !important;
                box-shadow: 0 2px 8px rgba(67, 56, 202, 0.18) !important;
            }}
            .stButton > button[kind="primary"]:hover {{
                box-shadow: 0 4px 12px rgba(67, 56, 202, 0.25) !important;
            }}

            /* === Botones secundarios === */
            .stButton > button[kind="secondary"] {{
                background: {C['surface2']} !important;
                color: {C['text2']} !important;
                border: 1px solid {C['border']} !important;
                font-weight: 500 !important;
                width: 140px !important;
                min-width: 140px !important;
                max-width: 140px !important;
                white-space: nowrap !important;
                padding: 10px 14px !important;
                font-size: 0.85rem !important;
            }}
            .stButton > button[kind="secondary"]:hover {{
                background: {C['border']} !important;
                color: {C['text']} !important;
            }}

            /* === Tabla: anchos FIJOS para alinear todas las filas === */
            [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .coef-table-marker) [data-testid="stHorizontalBlock"] {{
                flex-wrap: nowrap !important;
                justify-content: flex-start;
                gap: 6px !important;
            }}
            /* Columnas de variables (default): 90px fijos */
            [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .coef-table-marker) [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {{
                flex: 0 0 90px !important;
                width: 90px !important;
                min-width: 90px !important;
                max-width: 90px !important;
            }}
            /* Columna de etiqueta (Z, R1...): primera, más angosta */
            [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .coef-table-marker) [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(1) {{
                flex: 0 0 50px !important;
                width: 50px !important;
                min-width: 50px !important;
                max-width: 50px !important;
            }}
            /* Columna de tipo (selectbox o placeholder): penúltima, 95px para que quepa el operador */
            [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .coef-table-marker) [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-last-child(2) {{
                flex: 0 0 95px !important;
                width: 95px !important;
                min-width: 95px !important;
                max-width: 95px !important;
            }}
            /* Inputs llenan su columna (anchos ya están fijos) */
            [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .coef-table-marker) .stNumberInput,
            [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .coef-table-marker) .stSelectbox {{
                width: 100% !important;
                max-width: 100% !important;
                margin: 0 !important;
            }}
            [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .coef-table-marker) .stNumberInput input,
            [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .coef-table-marker) .stSelectbox > div > div {{
                min-width: 0 !important;
            }}

            /* === Chips de nombres de variables: ancho fijo de 130px === */
            [data-testid="stColumn"]:has([class*="st-key-var_name_"]) {{
                flex: 0 0 130px !important;
                width: 130px !important;
                min-width: 130px !important;
                max-width: 130px !important;
            }}

            /* === Botones de restricción: en una sola línea, fuera del scroll === */
            [data-testid="stElementContainer"]:has(.rest-btns-marker) + [data-testid="stElementContainer"] [data-testid="stHorizontalBlock"] {{
                flex-wrap: nowrap !important;
                gap: 8px !important;
            }}
            [data-testid="stElementContainer"]:has(.rest-btns-marker) + [data-testid="stElementContainer"] [data-testid="stColumn"]:nth-child(1),
            [data-testid="stElementContainer"]:has(.rest-btns-marker) + [data-testid="stElementContainer"] [data-testid="stColumn"]:nth-child(2) {{
                flex: 0 0 140px !important;
                min-width: 140px !important;
                width: 140px !important;
            }}

            /* === Expander === */
            [data-testid="stExpander"] {{
                border: 1px solid {C['border']} !important;
                border-radius: 10px !important;
                background: {C['surface']} !important;
                margin-bottom: 20px;
            }}
            [data-testid="stExpander"] summary {{
                font-family: 'DM Sans', sans-serif !important;
                color: {C['text2']} !important;
                font-size: 0.85rem !important;
                padding: 14px 20px !important;
            }}

            /* === Tabla de coeficientes === */
            .coef-table {{
                width: 100%;
                border-collapse: separate;
                border-spacing: 4px;
                margin-bottom: 12px;
            }}
            .coef-table th {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.72rem;
                color: {C['text3']};
                font-weight: 500;
                text-align: center;
                padding: 4px 2px 8px;
            }}
            .coef-table th.row-id {{ text-align: left; width: 40px; }}
            .coef-table td {{ text-align: center; vertical-align: middle; }}
            .coef-table td.row-id {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.78rem;
                font-weight: 600;
                color: {C['text2']};
                text-align: left;
                padding-left: 4px;
            }}
            .coef-table tr.fo-row td.row-id {{ color: {C['orange']}; }}

            /* === Result cards === */
            .result-z-wrap {{
                background: {C['surface2']};
                border: 1px solid {C['border']};
                border-left: 4px solid {C['indigo']};
                border-radius: 10px;
                padding: 20px 24px;
                margin: 16px 0;
            }}
            .result-z-label {{
                font-family: 'DM Sans', sans-serif;
                font-size: 0.72rem;
                color: {C['text2']};
                letter-spacing: 1.5px;
                text-transform: uppercase;
                margin-bottom: 6px;
            }}
            .result-z-value {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 2.4rem;
                font-weight: 600;
                color: {C['indigo']};
                letter-spacing: -1px;
                line-height: 1;
            }}

            .var-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
                gap: 8px;
                margin-bottom: 20px;
            }}
            .var-card {{
                background: {C['surface2']};
                border: 1px solid {C['border']};
                border-radius: 8px;
                padding: 12px 14px;
                text-align: center;
            }}
            .var-card-name {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.72rem;
                color: {C['text3']};
                margin-bottom: 4px;
            }}
            .var-card-val {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 1.15rem;
                font-weight: 600;
                color: {C['text']};
            }}

            /* === Tabla de restricciones en resultados === */
            .rest-table {{
                width: 100%;
                border-collapse: collapse;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.82rem;
            }}
            .rest-table th {{
                font-size: 0.68rem;
                color: {C['text3']};
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 1px;
                padding: 8px 12px;
                border-bottom: 1px solid {C['border']};
                text-align: left;
            }}
            .rest-table td {{
                padding: 10px 12px;
                border-bottom: 1px solid {C['border']};
                color: {C['text']};
            }}
            .rest-table tr:last-child td {{ border-bottom: none; }}
            .rest-table tr:hover td {{ background: {C['surface2']}; }}

            .badge {{
                display: inline-block;
                border-radius: 20px;
                padding: 5px 14px;
                font-family: 'DM Sans', sans-serif;
                font-size: 0.78rem;
                font-weight: 500;
            }}
            .badge-ok {{
                background: #dcfce7;
                color: #15803d;
                border: 1px solid #bbf7d0;
            }}
            .badge-err {{
                background: #fee2e2;
                color: #b91c1c;
                border: 1px solid #fecaca;
            }}
            .tag-active {{
                background: #ede9fe;
                color: {C['indigo']};
                border-radius: 5px;
                padding: 2px 9px;
                font-size: 0.72rem;
                font-weight: 500;
            }}
            .tag-inactive {{
                background: {C['surface2']};
                color: {C['text3']};
                border-radius: 5px;
                padding: 2px 9px;
                font-size: 0.72rem;
            }}

            hr {{ border-color: {C['border']} !important; }}
        </style>
    """, unsafe_allow_html=True)


def render_header():
    st.markdown(f"""
        <div style="margin-bottom: 32px;">
            <div style="
                font-family: 'DM Serif Display', serif;
                font-size: 3rem;
                color: {C['text']};
                line-height: 1;
                letter-spacing: -1px;
                margin-bottom: 8px;
            ">
                LP <span style="color:{C['indigo']};">Solver</span>
            </div>
            <div style="
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.75rem;
                color: {C['text3']};
                letter-spacing: 0.5px;
            ">
                linear programming optimizer &middot; powered by HiGHS &middot; v1.0.0
            </div>
        </div>
    """, unsafe_allow_html=True)


_HELP_HTML = (
f"""<div style="font-family:'DM Sans',sans-serif; color:{C['text2']}; font-size:0.9rem; line-height:1.7;">
<p><strong style="color:{C['text']};">Programación Lineal</strong> es una técnica de optimización matemática para encontrar el mejor resultado (máximo o mínimo) de una función lineal, dadas ciertas restricciones también lineales.</p>
<p style="font-family:'JetBrains Mono',monospace; font-size:0.82rem; background:{C['surface2']}; border-left:3px solid {C['indigo']}; border-radius:6px; padding:14px 18px; margin:12px 0; color:{C['text']}; line-height:1.9; white-space:pre;">max/min  Z = c₁·x₁ + c₂·x₂ + ... + cₙ·xₙ
s.a.     a₁₁·x₁ + a₁₂·x₂ + ... ≤ b₁
         a₂₁·x₁ + a₂₂·x₂ + ... ≥ b₂
         xᵢ ≥ 0   (no negatividad, implícita)</p>
<p><strong style="color:{C['text']};">Cómo usar:</strong> configura el número de variables y el sentido → ingresa los coeficientes en la tabla → presiona <strong>Resolver</strong>.</p>
<p><strong style="color:{C['text']};">Holgura:</strong> valor <code>RHS − LHS</code> de cada restricción. Si es ≈ 0, la restricción está <strong>Activa</strong> (cuello de botella). Si es &gt; 0, está <strong>Inactiva</strong> (recurso sobrante).</p>
</div>"""
)


def render_help():
    with st.expander("¿Cómo usar este solver?", expanded=False):
        st.markdown(_HELP_HTML, unsafe_allow_html=True)


def render_model_input():
    # === Sección 01: Configuración ===
    with st.container(border=True):
        st.markdown('<div class="section-title">01 · Configuración</div>',
                    unsafe_allow_html=True)

        col1, col2, _ = st.columns([1, 1, 3])
        with col1:
            n_vars = st.number_input(
                "Número de variables",
                min_value=1, max_value=20, value=2, step=1,
                key="n_vars"
            )
        with col2:
            sense = st.selectbox("Sentido", ["max", "min"], key="sense")

        # Nombres de variables como chips editables
        st.markdown(
            f'<div style="font-size:0.78rem;color:{C["text2"]};margin:12px 0 8px;">Nombres de variables</div>',
            unsafe_allow_html=True
        )
        var_names = []
        # Mostrar en filas de 8 columnas máximo
        chunk = 8
        for start in range(0, n_vars, chunk):
            end = min(start + chunk, n_vars)
            cols = st.columns(end - start)
            for i, col in enumerate(cols):
                idx = start + i
                with col:
                    name = st.text_input(
                        f"v{idx+1}", value=f"x{idx+1}",
                        key=f"var_name_{idx}",
                        label_visibility="collapsed"
                    )
                    var_names.append(name)

    # === Sección 02: Tabla de coeficientes ===
    with st.container(border=True):
        st.markdown('<div class="section-title">02 · Modelo</div>',
                    unsafe_allow_html=True)
        st.markdown(
            f'<div style="font-size:0.78rem;color:{C["text3"]};margin-bottom:14px;">'
            f'Ingresa los coeficientes de la función objetivo (Z) y cada restricción.</div>',
            unsafe_allow_html=True
        )

        if "n_restrictions" not in st.session_state:
            st.session_state.n_restrictions = 2

        n_rest = st.session_state.n_restrictions

        # Estilos dinámicos: min-width de la tabla + scroll horizontal si n_vars > 8
        # 96px por variable (90 + 6 gap) + 253px (label 50 + tipo 95 + RHS 90 + gaps)
        table_min_width = n_vars * 96 + 253
        overflow_css = (
            "overflow-x: auto !important; overflow-y: hidden !important;"
            if n_vars > 8 else ""
        )
        st.markdown(f"""
            <style>
            [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .coef-table-marker) {{
                {overflow_css}
            }}
            [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .coef-table-marker) > [data-testid="stElementContainer"] [data-testid="stHorizontalBlock"] {{
                min-width: {table_min_width}px !important;
            }}
            </style>
        """, unsafe_allow_html=True)

        # Contenedor de la tabla con scroll horizontal (los botones quedan fuera)
        with st.container():
            st.markdown('<div class="coef-table-marker"></div>',
                        unsafe_allow_html=True)

            # Encabezados de la tabla
            # Columnas: [etiqueta] + [var1..varN] + [tipo] + [RHS]
            header_cols = st.columns([0.6] + [1] * n_vars + [0.8] + [1])

            with header_cols[0]:
                st.markdown(
                    f'<div style="font-family:JetBrains Mono,monospace;font-size:0.68rem;'
                    f'color:{C["text3"]};padding-bottom:4px;text-align:center;white-space:nowrap;"></div>',
                    unsafe_allow_html=True
                )
            for i, col in enumerate(header_cols[1:n_vars+1]):
                with col:
                    st.markdown(
                        f'<div style="font-family:JetBrains Mono,monospace;font-size:0.72rem;'
                        f'color:{C["text3"]};text-align:center;padding-bottom:4px;white-space:nowrap;">'
                        f'{var_names[i]}</div>',
                        unsafe_allow_html=True
                    )
            with header_cols[n_vars+1]:
                st.markdown(
                    f'<div style="font-family:JetBrains Mono,monospace;font-size:0.72rem;'
                    f'color:{C["text3"]};text-align:center;padding-bottom:4px;white-space:nowrap;">tipo</div>',
                    unsafe_allow_html=True
                )
            with header_cols[n_vars+2]:
                st.markdown(
                    f'<div style="font-family:JetBrains Mono,monospace;font-size:0.72rem;'
                    f'color:{C["text3"]};text-align:center;padding-bottom:4px;white-space:nowrap;">RHS</div>',
                    unsafe_allow_html=True
                )

            # Fila de función objetivo (Z)
            obj_coeffs = []
            fo_cols = st.columns([0.6] + [1] * n_vars + [0.8] + [1])
            with fo_cols[0]:
                st.markdown(
                    f'<div style="font-family:JetBrains Mono,monospace;font-size:0.82rem;'
                    f'font-weight:600;color:{C["orange"]};padding-top:6px;text-align:center;white-space:nowrap;">Z</div>',
                    unsafe_allow_html=True
                )
            for i in range(n_vars):
                with fo_cols[i+1]:
                    c = st.number_input(
                        f"fo_{i}", value=1.0, key=f"obj_{i}",
                        format="%.2f", label_visibility="collapsed"
                    )
                    obj_coeffs.append(c)
            # Sin tipo ni RHS para FO
            with fo_cols[n_vars+1]:
                st.markdown('<div style="height:38px;"></div>', unsafe_allow_html=True)
            with fo_cols[n_vars+2]:
                st.markdown('<div style="height:38px;"></div>', unsafe_allow_html=True)

            # Línea separadora
            st.markdown(
                f'<hr style="margin:8px 0;border-color:{C["border"]};">',
                unsafe_allow_html=True
            )

            # Filas de restricciones
            restrictions = []
            for r in range(n_rest):
                r_cols = st.columns([0.6] + [1] * n_vars + [0.8] + [1])

                with r_cols[0]:
                    st.markdown(
                        f'<div style="font-family:JetBrains Mono,monospace;font-size:0.78rem;'
                        f'font-weight:600;color:{C["text2"]};padding-top:6px;text-align:center;white-space:nowrap;">'
                        f'R{r+1}</div>',
                        unsafe_allow_html=True
                    )

                coeffs = []
                for i in range(n_vars):
                    with r_cols[i+1]:
                        c = st.number_input(
                            f"r{r}_c{i}", value=1.0, key=f"r{r}_c{i}",
                            format="%.2f", label_visibility="collapsed"
                        )
                        coeffs.append(c)

                with r_cols[n_vars+1]:
                    r_type = st.selectbox(
                        f"tipo_r{r}", ["<=", ">=", "=="],
                        key=f"r{r}_type", label_visibility="collapsed"
                    )

                with r_cols[n_vars+2]:
                    rhs = st.number_input(
                        f"rhs_r{r}", value=10.0, key=f"r{r}_rhs",
                        format="%.2f", label_visibility="collapsed"
                    )

                restrictions.append(Restriction(
                    coefficients=coeffs, type=r_type, rhs=rhs
                ))

        # Botones agregar / quitar restricción (fuera del scroll de la tabla)
        st.markdown(
            '<div class="rest-btns-marker" style="margin-top:12px;"></div>',
            unsafe_allow_html=True
        )
        btn_col1, btn_col2, _ = st.columns([1, 1, 6])
        with btn_col1:
            if st.button("+ restricción", key="add_r", type="secondary"):
                st.session_state.n_restrictions += 1
                st.rerun()
        with btn_col2:
            if st.button("− restricción", key="rm_r", type="secondary") \
                    and st.session_state.n_restrictions > 1:
                st.session_state.n_restrictions -= 1
                st.rerun()

    return LPModel(
        sense=sense,
        objective_coefficients=obj_coeffs,
        variables=var_names,
        restrictions=restrictions
    )


def render_results(result):
    is_optimal = result.status == "Solución óptima encontrada"
    badge_class = "badge-ok" if is_optimal else "badge-err"

    with st.container(border=True):
        st.markdown('<div class="section-title">03 · Resultados</div>',
                    unsafe_allow_html=True)

        # Badge de estado
        st.markdown(
            f'<span class="badge {badge_class}">{result.status}</span>',
            unsafe_allow_html=True
        )

        if not is_optimal:
            return

        # Valor óptimo Z (HTML sin indentación: markdown trata >=4 espacios como código)
        st.markdown(
            f'<div class="result-z-wrap">'
            f'<div class="result-z-label">Valor óptimo</div>'
            f'<div class="result-z-value">Z = {result.objective_value}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        # Variables
        st.markdown(
            f'<div style="font-size:0.72rem;font-weight:600;color:{C["indigo"]};'
            f'letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;">Variables</div>',
            unsafe_allow_html=True
        )
        var_cards = "".join([
            f'<div class="var-card">'
            f'<div class="var-card-name">{name}</div>'
            f'<div class="var-card-val">{val}</div>'
            f'</div>'
            for name, val in result.variables.items()
        ])
        st.markdown(
            f'<div class="var-grid">{var_cards}</div>',
            unsafe_allow_html=True
        )

        # Tabla de restricciones
        st.markdown(
            f'<div style="font-size:0.72rem;font-weight:600;color:{C["indigo"]};'
            f'letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;">Restricciones</div>',
            unsafe_allow_html=True
        )

        rows = ""
        for r in result.restrictions:
            tag_class = "tag-active" if r["status"] == "Activa" else "tag-inactive"
            rows += (
                f'<tr>'
                f'<td style="color:{C["text2"]};font-weight:600;">{r["restriction"]}</td>'
                f'<td>{r["lhs"]}</td>'
                f'<td style="color:{C["text2"]};">{r["type"]}</td>'
                f'<td>{r["rhs"]}</td>'
                f'<td>{r["slack"]}</td>'
                f'<td><span class="{tag_class}">{r["status"]}</span></td>'
                f'</tr>'
            )

        st.markdown(
            f'<table class="rest-table">'
            f'<thead><tr>'
            f'<th>ID</th><th>LHS</th><th>Tipo</th>'
            f'<th>RHS</th><th>Holgura</th><th>Estado</th>'
            f'</tr></thead>'
            f'<tbody>{rows}</tbody>'
            f'</table>',
            unsafe_allow_html=True
        )


def render_empty_results():
    st.markdown(f"""
        <div style="
            text-align: center;
            padding: 48px 24px;
            color: {C['text3']};
            font-family: 'DM Sans', sans-serif;
            font-size: 0.88rem;
            border: 1px dashed {C['border2']};
            border-radius: 12px;
            margin-top: 8px;
        ">
            <div style="font-size:2rem;margin-bottom:12px;opacity:0.3;">∑</div>
            <div>Los resultados aparecerán aquí</div>
            <div style="font-size:0.78rem;color:{C['text3']};margin-top:6px;">
                Configura tu modelo y presiona Resolver
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_ai_input():
    # === Modo IA: el usuario describe el problema en lenguaje natural ===
    with st.container(border=True):
        st.markdown('<div class="section-title">01 · Describe tu problema</div>',
                    unsafe_allow_html=True)

        st.markdown(
            f'<div style="font-size:0.78rem;color:{C["text3"]};margin-bottom:14px;">'
            f'Describe el problema en lenguaje natural. La IA extraerá las variables, '
            f'la función objetivo y las restricciones automáticamente.</div>',
            unsafe_allow_html=True
        )

        # Key versionada: al limpiar se incrementa el contador, lo que fuerza
        # a Streamlit a montar el widget como nuevo (y por tanto vacío)
        textarea_version = st.session_state.get("ai_textarea_version", 0)
        problem_text = st.text_area(
            "Problema",
            placeholder=(
                "Ejemplo: Una fábrica produce sillas y mesas. "
                "Cada silla genera $3 de ganancia y toma 2 horas de trabajo. "
                "Cada mesa genera $5 y toma 3 horas. "
                "Hay 12 horas disponibles y máximo 4 sillas. "
                "¿Cuánto producir para maximizar la ganancia?"
            ),
            height=160,
            label_visibility="collapsed",
            key=f"ai_problem_text_{textarea_version}"
        )

        # Disclaimer estilo ChatGPT
        st.markdown(
            f'<div style="font-size:0.75rem;color:{C["text3"]};margin:10px 0 14px;'
            f'display:flex;align-items:flex-start;gap:8px;line-height:1.5;">'
            f'<span style="color:{C["orange"]};font-weight:700;font-size:0.85rem;'
            f'line-height:1;">!</span>'
            f'<span>La IA puede cometer errores al interpretar el problema. '
            f'Verifica el modelo extraído antes de confiar en los resultados.</span>'
            f'</div>',
            unsafe_allow_html=True
        )

        btn_solve_col, btn_clear_col, _ = st.columns([2, 1, 5])
        with btn_solve_col:
            if st.button("Interpretar y Resolver", type="primary", key="ai_solve_btn"):
                if not problem_text.strip():
                    st.warning("Por favor describe el problema antes de continuar.")
                else:
                    with st.spinner("Interpretando el problema..."):
                        from core.ai_parser import parse_problem
                        result = parse_problem(problem_text)

                        if "error" in result:
                            st.error(f"No se pudo interpretar el problema: {result['error']}")
                        else:
                            # Mostrar explicación de cómo interpretó la IA
                            st.session_state.ai_result = None
                            st.session_state.ai_model_display = result["model"]
                            st.session_state.ai_explanation = result["explanation"]

                            # Resolver el modelo
                            from core.solver import solve
                            st.session_state.ai_result = solve(result["model"])
        with btn_clear_col:
            st.button("Limpiar", key="ai_clear_btn",
                      on_click=clear_session_keep_mode)

    # Mostrar cómo interpretó la IA el modelo
    if "ai_explanation" in st.session_state and st.session_state.ai_explanation:
        with st.container(border=True):
            st.markdown('<div class="section-title">02 · Modelo interpretado</div>',
                        unsafe_allow_html=True)

            st.markdown(
                f'<div style="font-size:0.85rem;color:{C["text2"]};'
                f'background:{C["surface2"]};border-left:3px solid {C["indigo"]};'
                f'border-radius:6px;padding:12px 16px;margin-bottom:16px;">'
                f'{st.session_state.ai_explanation}</div>',
                unsafe_allow_html=True
            )

            # Mostrar el modelo extraído (todo el HTML en un solo st.markdown
            # para que el contenedor envuelva tanto Z como las restricciones)
            model = st.session_state.ai_model_display
            var_str = " + ".join([
                f"{c}·{v}"
                for c, v in zip(model.objective_coefficients, model.variables)
            ])
            rest_html = "".join(
                f'<div style="font-size:0.82rem;color:{C["text2"]};margin-top:4px;">'
                f'R{i+1}: '
                + " + ".join(
                    f"{c}·{v}" for c, v in zip(r.coefficients, model.variables)
                )
                + f' <span style="color:{C["text3"]};">{r.type}</span> {r.rhs}'
                + '</div>'
                for i, r in enumerate(model.restrictions)
            )
            st.markdown(
                f'<div style="font-family:JetBrains Mono,monospace;font-size:0.85rem;'
                f'color:{C["text"]};background:{C["surface2"]};border-radius:6px;'
                f'padding:14px 18px;line-height:1.8;">'
                f'<div><span style="color:{C["orange"]};font-weight:600;">{model.sense}</span> '
                f'Z = {var_str}</div>'
                f'{rest_html}'
                f'</div>',
                unsafe_allow_html=True
            )
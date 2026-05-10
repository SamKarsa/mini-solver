# app.py
import streamlit as st
from ui.componentes import apply_styles, render_header, render_model_input, render_results
from core.solver import solve

st.set_page_config(
    page_title="LP Solver",
    page_icon="🔢",
    layout="wide"
)

apply_styles()
render_header()

# Layout de dos columnas
col_input, col_results = st.columns([1, 1], gap="large")

with col_input:
    model = render_model_input()
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⚡ Resolver"):
        st.session_state.result = solve(model)

with col_results:
    if "result" in st.session_state and st.session_state.result:
        render_results(st.session_state.result)
    else:
        st.markdown("""
            <div style="
                height: 300px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #2a2d3a;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.85rem;
                border: 1px dashed #2a2d3a;
                border-radius: 12px;
            ">
                // los resultados aparecerán aquí
            </div>
        """, unsafe_allow_html=True)

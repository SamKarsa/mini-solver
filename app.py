# app.py
import streamlit as st
from ui.components import (
    apply_styles,
    render_header,
    render_help,
    render_model_input,
    render_ai_input,
    render_results,
    render_empty_results,
    clear_session_keep_mode,
)
from core.solver import solve

st.set_page_config(
    page_title="LP Solver",
    page_icon="⚡",
    layout="wide",
)

apply_styles()
render_header()
render_help()

# Selector de modo
mode = st.radio(
    "Modo",
    ["Manual", "IA"],
    horizontal=True,
    label_visibility="collapsed",
    key="mode"
)

st.markdown("<br>", unsafe_allow_html=True)

if mode == "Manual":
    model = render_model_input()

    st.markdown("<br>", unsafe_allow_html=True)

    btn_solve_col, btn_clear_col, _ = st.columns([2, 1, 5])
    with btn_solve_col:
        if st.button("Resolver", type="primary"):
            st.session_state.result = solve(model)
    with btn_clear_col:
        st.button("Limpiar", key="clear_btn",
                  on_click=clear_session_keep_mode)

    st.markdown("<br>", unsafe_allow_html=True)

    if "result" in st.session_state and st.session_state.result is not None:
        render_results(st.session_state.result)
    else:
        render_empty_results()

else:  # Modo IA
    render_ai_input()

    st.markdown("<br>", unsafe_allow_html=True)

    if "ai_result" in st.session_state and st.session_state.ai_result is not None:
        render_results(st.session_state.ai_result)
    else:
        render_empty_results()
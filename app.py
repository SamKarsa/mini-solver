# app.py
import streamlit as st
from ui.components import (
    apply_styles,
    render_header,
    render_help,
    render_model_input,
    render_results,
    render_empty_results,
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

model = render_model_input()

st.markdown("<br>", unsafe_allow_html=True)

btn_solve_col, btn_clear_col, _ = st.columns([2, 1, 5])
with btn_solve_col:
    if st.button("Resolver", type="primary"):
        st.session_state.result = solve(model)
with btn_clear_col:
    if st.button("Limpiar", key="clear_btn"):
        st.session_state.clear()
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

if "result" in st.session_state and st.session_state.result is not None:
    render_results(st.session_state.result)
else:
    render_empty_results()
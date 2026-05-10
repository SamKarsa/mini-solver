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
        render_empty_results()

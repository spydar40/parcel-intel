import streamlit as st
from app.login import show_login
from app.app import show_dashboard

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    show_login()
else:
    show_dashboard()

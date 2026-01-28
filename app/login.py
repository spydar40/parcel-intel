import streamlit as st
from pathlib import Path

# FIXED DEMO CREDENTIALS
VALID_USER = "customs_officer"
VALID_PASS = "dubai2026"

def show_login():
    # Page config MUST be first Streamlit call
    st.set_page_config(
        page_title="UAE Customs Login",
        layout="centered",
    )

    # ---------- WHITE BACKGROUND CSS ----------
    st.markdown(
        """
        <style>
        html, body, [data-testid="stApp"] {
            background-color: #ffffff !important;
            color: #000000 !important;
            height: 100%;
            margin: 0;
        }

        section.main > div {
            padding-top: 0rem;
        }

        .login-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            width: 100vw;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ---------- LAYOUT ----------
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    # ---------- LOGO ----------
    img_path = Path(__file__).parent / "images.jpg"
    st.image(img_path, width=130)

    st.markdown("<div class='title'>UAE Customs</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='subtitle'>PARCEL-INTEL — E-Commerce Intelligence Engine</div>",
        unsafe_allow_html=True
    )

    username = st.text_input("Officer ID", placeholder="Officer ID")
    password = st.text_input("Password", type="password", placeholder="Password")

    if st.button("Login", use_container_width=True):
        if username == VALID_USER and password == VALID_PASS:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.markdown("</div></div>", unsafe_allow_html=True)

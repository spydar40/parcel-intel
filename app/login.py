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

    # ---------- WHITE THEME CSS ----------
    st.markdown(
        """
        <style>
        html, body, [data-testid="stApp"] {
            background-color: #ffffff !important;
            color: #000000 !important;
            height: 100%;
            margin: 0;
            overflow: hidden;
            font-family: "Segoe UI", Arial, sans-serif;
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

        .title {
            font-size: 24px;
            font-weight: 600;
            margin-top: 12px;
        }

        .subtitle {
            font-size: 14px;
            margin-bottom: 24px;
        }

        div[data-baseweb="input"] > div {
            background-color: #111111 !important;
            border: 1px solid #000000 !important;
            border-radius: 6px !important;
        }

        input {
            color: #ffffff !important;
            background-color: #111111 !important;
            caret-color: #ffffff !important;
        }

        input::placeholder {
            color: #ffffff !important;
            opacity: 0.8 !important;
        }

        button[kind="primary"] {
            background-color: #000000 !important;
            color: #ffffff !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)

    # ---------- LOGO ----------
    img_path = Path(__file__).parent / "images.jpg"
    st.image(img_path, width=130)

    st.markdown("<div class='title'>UAE Customs</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Secure Login</div>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", type="primary"):
        if username == VALID_USER and password == VALID_PASS:
            st.success("Login successful")
            st.session_state["authenticated"] = True
        else:
            st.error("Invalid credentials")

    st.markdown("</div>", unsafe_allow_html=True)

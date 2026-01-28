import streamlit as st

import streamlit as st

st.markdown("""
<style>
/* Page background (optional – keep dark login look) */
.stApp {
    background-color: #0e1117;
}

/* All text */
html, body, [class*="css"]  {
    color: white !important;
}

/* Input labels */
label {
    color: white !important;
    font-weight: 500;
}

/* Text inputs */
input {
    color: white !important;
    background-color: #1c1f26 !important;
}

/* Placeholder text */
input::placeholder {
    color: #b0b3b8 !important;
}

/* Buttons */
button {
    color: white !important;
    background-color: black !important;
    border-radius: 6px;
}

/* Error / warning messages */
.stAlert {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)


# FIXED DEMO CREDENTIALS
VALID_USER = "customs_officer"
VALID_PASS = "dubai2026"

def show_login():
    st.set_page_config(
        page_title="UAE Customs Login",
        layout="centered"
    )

    # ---------- HARD OVERRIDE CSS ----------
    st.markdown(
        """
        <style>
        /* Force light theme */
        html, body, [data-testid="stApp"] {
            background-color: #ffffff !important;
            color: #000000 !important;
            height: 100%;
            margin: 0;
            overflow: hidden;
            font-family: "Segoe UI", Arial, sans-serif;
        }

        /* Remove Streamlit padding */
        section.main > div {
            padding-top: 0rem;
        }

        /* Center wrapper */
        .login-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            width: 100vw;
        }

       
        /* Titles */
        .title {
            font-size: 24px;
            font-weight: 600;
            color: #000000;
            margin-top: 12px;
        }

        .subtitle {
            font-size: 14px;
            color: #000000;
            margin-bottom: 24px;
        }

        /* Input wrapper */
        div[data-baseweb="input"] > div {
            background-color: #111111 !important;
            border: 1px solid #000000 !important;
            border-radius: 6px !important;
        }

        /* Input text */
        input {
            color: #ffffff !important;
            background-color: #111111 !important;
            caret-color: #ffffff !important;
        }

        /* Placeholder */
        input::placeholder {
            color: #ffffff !important;
            opacity: 0.8 !important;
        }

        /* Password eye */
        button[data-testid="stPasswordToggle"] {
            background-color: #111111 !important;
            border-left: 1px solid #000000 !important;
        }

        button[data-testid="stPasswordToggle"] svg {
            fill: #ffffff !important;
            color: #ffffff !important;
        }

        /* Login button */
        button[kind="primary"] {
            background-color: #ffffff !important;
            color: #ffffff !important;
            border: 1px solid #000000 !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
        }

        button[kind="primary"] * {
            color: #ffffff !important;
        }

        button[kind="primary"]:hover {
            background-color: #f0f0f0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ---------- LAYOUT ----------
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    # LOGO
    st.image(
        r"C:\Users\USER\Desktop\WCO_Ecommerce\images.jpg",
        width=130
    )

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

import sys
from pathlib import Path
import streamlit as st
import pandas as pd

# --------------------------------------------------
# STREAMLIT CONFIG (MUST BE FIRST)
# --------------------------------------------------
st.set_page_config(
    page_title="PARCEL-INTEL — UAE Customs",
    layout="wide"
)

# --------------------------------------------------
# FIX PYTHON PATH (FOR src/)
# --------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.data_loader import load_orders
from src.pipeline import run_customs_engine

# --------------------------------------------------
# AUTH STATE (TEMP SIMPLE)
# --------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = True  # skip login for now

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------
def show_dashboard():
    st.markdown(
        """
        <style>
        html, body, [data-testid="stApp"] {
            background-color: #ffffff;
            color: #000000;
            font-family: "Segoe UI", Arial, sans-serif;
        }
        .kpi-card {
            border: 1px solid #dcdcdc;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }
        .kpi-title {
            font-size: 14px;
            color: #555;
        }
        .kpi-value {
            font-size: 28px;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # HEADER
    col1, col2 = st.columns([1, 8])

    with col1:
        img_path = Path(__file__).parent / "images.jpg"
        if img_path.exists():
            st.image(img_path, width=80)

    with col2:
        st.markdown("## PARCEL-INTEL — UAE Customs")
        st.caption("E-Commerce Intelligence & Decision Support")

    st.divider()

    # DATA
    orders = load_orders(ROOT_DIR)
    results = run_customs_engine(orders)

    # KPIs
    k1, k2, k3, k4 = st.columns(4)

    k1.markdown(f"<div class='kpi-card'><div class='kpi-title'>Parcels</div><div class='kpi-value'>{len(results)}</div></div>", unsafe_allow_html=True)
    k2.markdown(f"<div class='kpi-card'><div class='kpi-title'>Split Alerts</div><div class='kpi-value'>{int(results['split_shipment_flag'].sum())}</div></div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='kpi-card'><div class='kpi-title'>High Risk</div><div class='kpi-value'>{int(results['risk_flag'].sum())}</div></div>", unsafe_allow_html=True)
    k4.markdown(f"<div class='kpi-card'><div class='kpi-title'>Total Duty (AED)</div><div class='kpi-value'>{round(results['duty_aed'].sum(),2)}</div></div>", unsafe_allow_html=True)

    st.divider()

    # TABLE
    st.subheader("📦 Customs Decisions")
    st.dataframe(results, use_container_width=True)

    # LOGOUT
    col_empty, col_logout = st.columns([8, 2])
    with col_logout:
        if st.button("🔒 Logout"):
            st.session_state.clear()
            st.rerun()

# --------------------------------------------------
# APP ENTRY
# --------------------------------------------------
if st.session_state.authenticated:
    show_dashboard()
else:
    st.write("Login disabled for now")

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
# SIMPLE AUTH (TEMP)
# --------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = True

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------
def show_dashboard():

    # -------------------------
    # CSS
    # -------------------------
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
            padding: 18px;
            text-align: center;
        }

        .kpi-title {
            font-size: 13px;
            color: #555;
        }

        .kpi-value {
            font-size: 26px;
            font-weight: 600;
        }

        button {
            color: #ffffff !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # -------------------------
    # HEADER
    # -------------------------
    col_logo, col_title = st.columns([1, 8])

    with col_logo:
        img_path = Path(__file__).parent / "images.jpg"
        if img_path.exists():
            st.image(img_path, width=80)

    with col_title:
        st.markdown("## PARCEL-INTEL — UAE CUSTOMS")
        st.caption("E-Commerce Intelligence & Decision Support Platform")

    st.divider()

    # -------------------------
    # LOAD DATA
    # -------------------------
    orders = load_orders(ROOT_DIR)
    results = run_customs_engine(orders)

    # REMOVE UNNAMED COLUMNS
    results = results.loc[:, ~results.columns.str.contains("^Unnamed")]

    # -------------------------
    # KPIs
    # -------------------------
    k1, k2, k3, k4 = st.columns(4)

    k1.markdown(f"<div class='kpi-card'><div class='kpi-title'>Parcels Processed</div><div class='kpi-value'>{len(results)}</div></div>", unsafe_allow_html=True)
    k2.markdown(f"<div class='kpi-card'><div class='kpi-title'>Split Shipment Alerts</div><div class='kpi-value'>{int(results['split_shipment_flag'].sum())}</div></div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='kpi-card'><div class='kpi-title'>High-Risk Items</div><div class='kpi-value'>{int(results['risk_flag'].sum())}</div></div>", unsafe_allow_html=True)
    k4.markdown(f"<div class='kpi-card'><div class='kpi-title'>Total Duty (AED)</div><div class='kpi-value'>{round(results['duty_aed'].sum(), 2)}</div></div>", unsafe_allow_html=True)

    st.divider()

    # -------------------------
    # TABLE (SAFE SIZE)
    # -------------------------
    st.subheader("📦 Customs Decisions (Operational View)")

    decision_columns = [
        "order_id",
        "importer_name",
        "product_title",
        "predicted_hs_code",
        "item_value_aed",
        "daily_total_value_aed",
        "split_shipment_flag",
        "duty_aed",
        "risk_category",
        "assigned_risk_lane",
    ]

    st.dataframe(
        results[decision_columns].head(1000),
        use_container_width=True,
        height=420
    )

    # -------------------------
    # DOWNLOAD
    # -------------------------
    csv = results[decision_columns].to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Customs Decision CSV",
        data=csv,
        file_name="customs_decisions.csv",
        mime="text/csv"
    )

    st.divider()

    # -------------------------
    # LOGOUT
    # -------------------------
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
    st.write("Login disabled")

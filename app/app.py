import sys
from pathlib import Path
import streamlit as st
import pandas as pd

from src.data_loader import load_orders
from src.pipeline import run_customs_engine

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))


def show_dashboard():
    # -------------------------
    # PAGE CONFIG
    # -------------------------
    st.set_page_config(
        page_title="PARCEL-INTEL — UAE Customs",
        layout="wide"
    )

    # -------------------------
    # GLOBAL WHITE GOVERNMENT CSS (SAFE)
    # -------------------------
    st.markdown(
        """
        <style>
        html, body, [data-testid="stApp"] {
            background-color: #ffffff !important;
            color: #000000 !important;
            font-family: "Segoe UI", Arial, sans-serif;
        }

        .kpi-card {
            background-color: #ffffff !important;
            border: 1px solid #dcdcdc !important;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }

        .kpi-title {
            font-size: 14px;
            color: #555555 !important;
            font-weight: 500;
        }

        .kpi-value {
            font-size: 28px;
            font-weight: 600;
            color: #000000 !important;
        }

        div[data-testid="stDownloadButton"] button {
            background-color: #1f4fd8 !important;
            color: #ffffff !important;
            font-weight: 600;
            border-radius: 6px;
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
        st.image(
            r"C:\Users\USER\Desktop\WCO_Ecommerce\images.jpg",
            width=90
        )

    with col_title:
        st.markdown(
            "<h2>PARCEL-INTEL — UAE Customs E-Commerce Intelligence Engine</h2>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<span style='color:#555555'>Royal Customs Decision Support Platform</span>",
            unsafe_allow_html=True
        )

    st.divider()

    # -------------------------
    # LOAD & PROCESS DATA
    # -------------------------
    orders = load_orders(BASE_DIR)
    results = run_customs_engine(orders)

    # -------------------------
    # KPI VALUES (PRECOMPUTED — SAFE)
    # -------------------------
    total_parcels = len(results)
    split_alerts = int(results["split_shipment_flag"].sum())
    high_risk = int(results["risk_flag"].sum())
    total_duty = round(float(results["duty_aed"].sum()), 2)

    # -------------------------
    # KPI CARDS
    # -------------------------
    k1, k2, k3, k4 = st.columns(4)

    k1.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Parcels Processed</div>
            <div class="kpi-value">{total_parcels}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    k2.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Split Shipment Alerts</div>
            <div class="kpi-value">{split_alerts}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    k3.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">High-Risk Items</div>
            <div class="kpi-value">{high_risk}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    k4.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Duty Assessed (AED)</div>
            <div class="kpi-value">{total_duty}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # -------------------------
    # ANALYTICS
    # -------------------------
    st.subheader("📊 Intelligence Overview")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.caption("Risk Lane Distribution")
        st.bar_chart(results["assigned_risk_lane"].value_counts())

    with c2:
        st.caption("Duty vs Exempt Items")
        st.bar_chart(results["duty_status"].value_counts())

    with c3:
        st.caption("Daily Parcel Volume")
        daily = results.groupby("order_date").size()
        st.line_chart(daily)

    st.divider()

    # -------------------------
    # OPERATIONAL TABLE
    # -------------------------
    st.subheader("📦 Item-Level Customs Decisions")

    st.dataframe(
        results[
            [
                "order_id",
                "importer_name",
                "product_title",
                "predicted_hs_code",
                "item_value_aed",
                "daily_total_value_aed",
                "split_shipment_flag",
                "duty_aed",
                "risk_category",
                "assigned_risk_lane"
            ]
        ],
        use_container_width=True,
        height=420
    )

    # -------------------------
    # EXPORT
    # -------------------------
    csv = results.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Export Official Customs Decision File",
        csv,
        "dubai_customs_parcel_intel.csv",
        "text/csv"
    )
st.divider()

st.markdown("<br>", unsafe_allow_html=True)

col_empty, col_logout = st.columns([8, 2])

with col_logout:
    if st.button("🔒 Logout"):
        st.session_state.clear()
        st.rerun()

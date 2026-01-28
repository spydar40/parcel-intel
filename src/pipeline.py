import pandas as pd
import numpy as np

from src.config import INR_TO_AED, DE_MINIMIS_AED, DEFAULT_TARIFF_RATE, RISK_KEYWORDS


def run_customs_engine(orders: pd.DataFrame) -> pd.DataFrame:
    # -------------------------
    # PREP
    # -------------------------
    orders = orders.copy()

    orders["timestamp"] = pd.to_datetime(orders["timestamp"])
    orders["order_date"] = orders["timestamp"].dt.date

    orders["item_price_inr"] = (
        orders["item_price_inr"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.extract(r"(\d+\.?\d*)")[0]
        .astype(float)
    )

    orders["item_value_aed"] = orders["item_price_inr"] * INR_TO_AED

    # -------------------------
    # LEVEL 1 — IDENTITY ENGINE
    # -------------------------
    daily_totals = (
        orders
        .groupby(
            ["importer_name", "delivery_address", "order_date"],
            as_index=False
        )
        .agg(daily_total_value_aed=("item_value_aed", "sum"))
    )

    orders = orders.merge(
        daily_totals,
        on=["importer_name", "delivery_address", "order_date"],
        how="left"
    )

    orders["split_shipment_flag"] = orders["daily_total_value_aed"] > DE_MINIMIS_AED

    # -------------------------
    # LEVEL 2 — HS CLASSIFICATION
    # -------------------------
    HS_MAP = {
        "6203.42": ["jeans", "trousers", "pants"],
        "6109.10": ["t-shirt", "tshirt"],
        "8507.60": ["lithium", "battery", "power bank"],
        "8806.00": ["drone", "uav", "quadcopter"],
        "7113.19": ["gold", "diamond", "jewellery"]
    }

    def classify_hs(text: str) -> str:
        text = text.lower()
        for hs, keywords in HS_MAP.items():
            if any(k in text for k in keywords):
                return hs
        return "9999.99"

    orders["classification_text"] = (
        orders["product_title"].fillna("") + " " +
        orders["description"].fillna("") + " " +
        orders["product_category"].fillna("")
    )

    orders["predicted_hs_code"] = orders["classification_text"].apply(classify_hs)

    # -------------------------
    # LEVEL 3 — VALUATION ENGINE
    # -------------------------
    orders["tariff_rate"] = DEFAULT_TARIFF_RATE

    orders["duty_aed"] = np.where(
        orders["daily_total_value_aed"] <= DE_MINIMIS_AED,
        0,
        orders["item_value_aed"] * orders["tariff_rate"]
    )

    orders["duty_status"] = np.where(
        orders["duty_aed"] == 0,
        "EXEMPT",
        "DUE"
    )

    # -------------------------
    # LEVEL 4 — PROTECTION ENGINE
    # -------------------------
    def risk_scan(text: str) -> str:
        text = text.lower()
        for risk, keywords in RISK_KEYWORDS.items():
            if any(k in text for k in keywords):
                return risk
        return "NONE"

    orders["risk_category"] = orders["classification_text"].apply(risk_scan)
    orders["risk_flag"] = orders["risk_category"] != "NONE"

    # -------------------------
    # RISK LANE ASSIGNMENT
    # -------------------------
    def assign_risk_lane(row) -> str:
        if row["risk_category"] in ["WEAPON", "DRONE"]:
            return "BLACK"
        if row["split_shipment_flag"] or row["risk_category"] == "LITHIUM_BATTERY":
            return "RED"
        if row["predicted_hs_code"] == "9999.99":
            return "YELLOW"
        return "GREEN"

    orders["assigned_risk_lane"] = orders.apply(assign_risk_lane, axis=1)

    return orders

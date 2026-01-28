from pathlib import Path
import pandas as pd
import numpy as np

from src.config import INR_TO_AED, DE_MINIMIS_AED, DEFAULT_TARIFF_RATE
from src.data_loader import load_orders

# -------------------------------------------------
# BASE DIRECTORY
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
orders = load_orders(BASE_DIR)

# -------------------------------------------------
# PREP & NORMALIZATION
# -------------------------------------------------
orders["timestamp"] = pd.to_datetime(orders["timestamp"])
orders["order_date"] = orders["timestamp"].dt.date

# Clean price field (strings → numbers)
orders["item_price_inr"] = (
    orders["item_price_inr"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.extract(r"(\d+\.?\d*)")[0]
    .astype(float)
)

# Currency conversion
orders["item_value_aed"] = orders["item_price_inr"] * INR_TO_AED

# -------------------------------------------------
# LEVEL 1 — IDENTITY ENGINE (SPLIT SHIPMENTS)
# -------------------------------------------------
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

# -------------------------------------------------
# LEVEL 3 — VALUATION ENGINE (DE MINIMIS & DUTY)
# -------------------------------------------------
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

# -------------------------------------------------
# OUTPUT
# -------------------------------------------------
output_cols = [
    "order_id",
    "importer_name",
    "order_date",
    "product_title",
    "item_value_aed",
    "daily_total_value_aed",
    "split_shipment_flag",
    "duty_aed",
    "duty_status"
]

output = orders[output_cols]

output_path = BASE_DIR / "data" / "processed" / "customs_intelligence_output.csv"
output.to_csv(output_path, index=False)

print("MAX daily total AED:", output["daily_total_value_aed"].max())
print("Importer-days > 1000 AED:", (output["daily_total_value_aed"] > 1000).sum())


print("✅ Pipeline executed successfully")
print(f"📄 Output written to: {output_path}")

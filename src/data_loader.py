import pandas as pd
from pathlib import Path

def load_orders(base_dir: Path) -> pd.DataFrame:
    path = base_dir / "data" / "raw" / "ecommerce_orders.xlsx"
    df = pd.read_excel(path)
    return df

def load_tariff(base_dir: Path) -> pd.DataFrame:
    path = base_dir / "data" / "raw" / "tariff.csv"
    df = pd.read_csv(path)
    return df

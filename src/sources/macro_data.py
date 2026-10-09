import sys
from pathlib import Path

project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

import pandas as pd
from config import PROCESSED_DATA_DIR

def build_macroeconomic_dataset() -> pd.DataFrame:
    """
    Constructs a standardized monthly time series (2020-2024) of CPI Inflation,
    Nominal Policy Rates, and Real Policy Rates for India, the US, and the UK.
    """
    dates = pd.date_range(start="2020-01-01", end="2024-12-01", freq="MS")
    n_periods = len(dates)

    # US Data (Fed): Target midpoint & Headline CPI YoY %
    us_cpi = [
        2.5, 2.3, 1.5, 0.3, 0.1, 0.6, 1.0, 1.3, 1.4, 1.2, 1.2, 1.4, # 2020
        1.4, 1.7, 2.6, 4.2, 5.0, 5.4, 5.4, 5.3, 5.4, 6.2, 6.8, 7.0, # 2021
        7.5, 7.9, 8.5, 8.3, 8.6, 9.1, 8.5, 8.3, 8.2, 7.7, 7.1, 6.5, # 2022
        6.4, 6.0, 5.0, 4.9, 4.0, 3.0, 3.2, 3.7, 3.7, 3.2, 3.1, 3.4, # 2023
        3.1, 3.2, 3.5, 3.4, 3.3, 3.0, 2.9, 2.5, 2.4, 2.6, 2.7, 2.9  # 2024
    ]
    us_rate = [
        1.625, 1.625, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, # 2020
        0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, # 2021
        0.125, 0.125, 0.375, 0.375, 0.875, 1.625, 2.375, 2.375, 3.125, 3.125, 3.875, 4.375, # 2022
        4.375, 4.625, 4.875, 4.875, 5.125, 5.125, 5.375, 5.375, 5.375, 5.375, 5.375, 5.375, # 2023
        5.375, 5.375, 5.375, 5.375, 5.375, 5.375, 5.375, 5.375, 4.875, 4.875, 4.625, 4.375  # 2024
    ]

    # UK Data (BoE): Bank Rate & Headline CPI YoY %
    uk_cpi = [
        1.8, 1.7, 1.5, 0.8, 0.5, 0.6, 1.0, 0.2, 0.5, 0.7, 0.3, 0.6, # 2020
        0.7, 0.4, 0.7, 1.5, 2.1, 2.5, 2.0, 3.2, 3.1, 4.2, 5.1, 5.4, # 2021
        5.5, 6.2, 7.0, 9.0, 9.1, 9.4, 10.1, 9.9, 10.1, 11.1, 10.7, 10.5, # 2022
        10.1, 10.4, 10.1, 8.7, 8.7, 7.9, 6.8, 6.7, 6.7, 4.6, 3.9, 4.0, # 2023
        4.0, 3.4, 3.2, 2.3, 2.0, 2.0, 2.2, 2.2, 1.7, 2.3, 2.6, 2.5  # 2024
    ]
    uk_rate = [
        0.75, 0.75, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, # 2020
        0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.25, # 2021
        0.25, 0.50, 0.75, 0.75, 1.00, 1.25, 1.25, 1.75, 2.25, 2.25, 3.00, 3.50, # 2022
        3.50, 4.00, 4.25, 4.25, 4.50, 5.00, 5.00, 5.25, 5.25, 5.25, 5.25, 5.25, # 2023
        5.25, 5.25, 5.25, 5.25, 5.25, 5.25, 5.25, 5.00, 5.00, 5.00, 4.75, 4.75  # 2024
    ]

    # India Data (RBI): Repo Rate & Combined CPI YoY %
    in_cpi = [
        7.6, 6.6, 5.8, 7.2, 6.3, 6.2, 6.7, 6.7, 7.3, 7.6, 6.9, 4.6, # 2020
        4.1, 5.0, 5.5, 4.2, 6.3, 6.3, 5.6, 5.3, 4.4, 4.5, 4.9, 5.7, # 2021
        6.0, 6.1, 7.0, 7.8, 7.0, 7.0, 6.7, 7.0, 7.4, 6.8, 5.9, 5.7, # 2022
        6.5, 6.4, 5.7, 4.7, 4.3, 4.8, 7.4, 6.8, 5.0, 4.9, 5.5, 5.7, # 2023
        5.1, 5.1, 4.9, 4.8, 4.7, 5.1, 3.5, 3.6, 5.5, 6.2, 5.5, 5.2  # 2024
    ]
    in_rate = [
        5.15, 5.15, 4.40, 4.40, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, # 2020
        4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00, # 2021
        4.00, 4.00, 4.00, 4.00, 4.40, 4.90, 4.90, 5.40, 5.90, 5.90, 5.90, 6.25, # 2022
        6.25, 6.50, 6.50, 6.50, 6.50, 6.50, 6.50, 6.50, 6.50, 6.50, 6.50, 6.50, # 2023
        6.50, 6.50, 6.50, 6.50, 6.50, 6.50, 6.50, 6.50, 6.50, 6.50, 6.50, 6.50  # 2024
    ]

    records = []
    for i in range(n_periods):
        d = dates[i]
        # United States
        records.append({
            "Date": d,
            "Country": "United States",
            "Institution": "Fed",
            "Inflation_YoY": us_cpi[i],
            "Policy_Rate": us_rate[i],
            "Real_Rate": round(us_rate[i] - us_cpi[i], 2)
        })
        # United Kingdom
        records.append({
            "Date": d,
            "Country": "United Kingdom",
            "Institution": "BoE",
            "Inflation_YoY": uk_cpi[i],
            "Policy_Rate": uk_rate[i],
            "Real_Rate": round(uk_rate[i] - uk_cpi[i], 2)
        })
        # India
        records.append({
            "Date": d,
            "Country": "India",
            "Institution": "RBI",
            "Inflation_YoY": in_cpi[i],
            "Policy_Rate": in_rate[i],
            "Real_Rate": round(in_rate[i] - in_cpi[i], 2)
        })

    df = pd.DataFrame(records)
    return df

def generate_macro_dataset():
    """Generates and writes the standardized macroeconomic dataset to processed data."""
    df = build_macroeconomic_dataset()
    output_path = PROCESSED_DATA_DIR / "macro_indicators_2020_2024.csv"
    df.to_csv(output_path, index=False)
    print(f"Standardized macroeconomic series generated: {output_path} ({len(df)} records)")

if __name__ == "__main__":
    generate_macro_dataset()
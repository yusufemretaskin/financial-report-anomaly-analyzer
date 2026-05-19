from pathlib import Path
import pandas as pd


THRESHOLDS = {
    "cash_balance": 50000,
    "variation_margin": 10000,
    "initial_margin": 5000,
    "pnl": 5000
}

GROUP_COLUMNS = ["account", "clearer", "product"]


def analyze_report(file_path: Path) -> dict:
    df = pd.read_csv(file_path)

    required_columns = [
        "date",
        "account",
        "clearer",
        "product",
        "currency",
        "cash_balance",
        "variation_margin",
        "initial_margin",
        "pnl"
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        return {
            "error": "Missing required columns",
            "missing_columns": missing_columns
        }

    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values(GROUP_COLUMNS + ["date"])

    for column in THRESHOLDS.keys():
        df[f"{column}_change"] = df.groupby(GROUP_COLUMNS)[column].diff()

    anomalies = []

    for _, row in df.iterrows():
        reasons = []

        for column, threshold in THRESHOLDS.items():
            change_value = row[f"{column}_change"]

            if pd.notna(change_value) and abs(change_value) >= threshold:
                reasons.append({
                    "field": column,
                    "change": float(change_value),
                    "threshold": threshold
                })

        if reasons:
            anomalies.append({
                "date": row["date"].strftime("%Y-%m-%d"),
                "account": row["account"],
                "clearer": row["clearer"],
                "product": row["product"],
                "currency": row["currency"],
                "cash_balance": float(row["cash_balance"]),
                "variation_margin": float(row["variation_margin"]),
                "initial_margin": float(row["initial_margin"]),
                "pnl": float(row["pnl"]),
                "reasons": reasons
            })

    return {
        "row_count": int(len(df)),
        "anomaly_count": len(anomalies),
        "anomalies": anomalies
    }
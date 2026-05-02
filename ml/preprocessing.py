import pandas as pd
from sklearn.preprocessing import StandardScaler


def load_data():
    return pd.read_csv("data/courier_data.csv")


def preprocess(df):

    df = df.copy()

    # ==============================
    # CREATE PROPER TARGET (FIX)
    # ==============================
    # Define burnout based on realistic logic
    df["burnout_risk"] = (
        (df["stress_level"] > 7) &
        (df["weekly_hours"] > 55) &
        (df["income_variability"] > 0.4)
    ).astype(int)

    print("\nNew burnout distribution:")
    print(df["burnout_risk"].value_counts())

    # ==============================
    # ENCODE CITY
    # ==============================
    if "city" in df.columns:
        df = pd.get_dummies(df, columns=["city"], drop_first=True)

    # ==============================
    # FEATURE ENGINEERING
    # ==============================
    df["workload"] = df["weekly_hours"] * df["deliveries_per_week"]
    df["stress_ratio"] = df["stress_level"] / (df["work_life_balance"] + 1)

    # ==============================
    # DROP UNUSED
    # ==============================
    drop_cols = ["courier_id", "burnout_score"]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    # ==============================
    # SPLIT
    # ==============================
    X = df.drop("burnout_risk", axis=1)
    y = df["burnout_risk"]

    # ==============================
    # SCALE
    # ==============================
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler, X.columns
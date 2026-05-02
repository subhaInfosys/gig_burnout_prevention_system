import joblib
import pandas as pd

# ==============================
# LOAD ARTIFACTS (ONCE)
# ==============================
model = joblib.load("artifacts/model.pkl")
scaler = joblib.load("artifacts/scaler.pkl")
feature_names = joblib.load("artifacts/features.pkl")


# ==============================
# PREDICTION FUNCTION
# ==============================
def predict(data: dict):

    try:
        # --------------------------
        # INPUT → DATAFRAME
        # --------------------------
        df = pd.DataFrame([data])

        # --------------------------
        # TYPE CAST (SAFE)
        # --------------------------
        numeric_cols = [
            "weekly_hours",
            "deliveries_per_week",
            "weekly_income",
            "income_variability",
            "stress_level",
            "work_life_balance",
            "job_satisfaction",
            "experience_years"
        ]

        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # --------------------------
        # FEATURE ENGINEERING
        # --------------------------
        df["workload"] = df["weekly_hours"] * df["deliveries_per_week"]
        df["stress_ratio"] = df["stress_level"] / (df["work_life_balance"] + 1)

        # --------------------------
        # ENCODING (SAFE)
        # --------------------------
        df = pd.get_dummies(df)

        # --------------------------
        # ALIGN FEATURES
        # --------------------------
        df = df.reindex(columns=feature_names, fill_value=0)

        # --------------------------
        # SCALE
        # --------------------------
        X_scaled = scaler.transform(df)

        # --------------------------
        # PREDICT
        # --------------------------
        prediction = model.predict(X_scaled)[0]

        return int(prediction)

    except Exception as e:
        print(f"Prediction error: {e}")
        return 0  # fallback

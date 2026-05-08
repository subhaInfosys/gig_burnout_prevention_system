import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# ==============================
# FIX IMPORT PATH
# ==============================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ==============================
# IMPORT MODEL (NO API)
# ==============================
from backend.model_service import predict

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="WIBPS Dashboard", layout="wide")

st.markdown("""
    <style>
    button[kind="header"] {display: none;}
    .stDeployButton {display: none;}
    </style>
""", unsafe_allow_html=True)

# ==============================
# LOAD DATA
# ==============================
df = pd.read_csv("data/model_output.csv")

# ==============================
# SIDEBAR
# ==============================
st.sidebar.header("🔎 Filters")

orders_range = st.sidebar.slider(
    "Total Orders",
    0,
    int(df["total_orders"].max()),
    (0, int(df["total_orders"].max()))
)

night_range = st.sidebar.slider(
    "Night Orders",
    0,
    int(df["night_orders"].max()),
    (0, int(df["night_orders"].max()))
)

burnout_filter = st.sidebar.selectbox(
    "Burnout Level",
    ["All", "Low", "Medium", "High"]
)

# ==============================
# APPLY FILTERS
# ==============================
filtered_df = df[
    (df["total_orders"].between(*orders_range)) &
    (df["night_orders"].between(*night_range))
]

if burnout_filter != "All":
    filtered_df = filtered_df[filtered_df["burnout_level"] == burnout_filter]

# ==============================
# HEADER
# ==============================
st.title("📊 Workforce Insight & Burnout Prevention System (WIBPS)")
st.markdown("### Real-Time Gig Worker Burnout Intelligence")
st.markdown("---")

# ==============================
# KPI SECTION
# ==============================
col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Riders", len(filtered_df))
col2.metric("📦 Avg Orders", round(filtered_df["total_orders"].mean(), 1))
col3.metric("🌙 Night Orders", round(filtered_df["night_orders"].mean(), 1))
col4.metric(
    "🔥 High Risk %",
    f"{round((filtered_df['burnout_level']=='High').mean()*100, 2)}%"
)

# ==============================
# TABS
# ==============================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "🔥 Burnout Analysis",
    "⚡ Workload Insights",
    "🎯 Prediction",
    "📈 Segmentation"
])

# ==============================
# TAB 1 — OVERVIEW
# ==============================
with tab1:
    fig = px.scatter(
        filtered_df,
        x="workload_index",
        y="burnout_score",
        color="burnout_level",
        size="total_orders",
        hover_data=["rider_id"]
    )
    st.plotly_chart(fig, use_container_width=True)

# ==============================
# TAB 2 — BURNOUT
# ==============================
with tab2:
    fig = px.box(
        filtered_df,
        x="burnout_level",
        y="burnout_score",
        color="burnout_level"
    )
    st.plotly_chart(fig, use_container_width=True)

# ==============================
# TAB 3 — WORKLOAD
# ==============================
with tab3:
    fig = px.scatter(
        filtered_df,
        x="avg_order_value",
        y="burnout_score",
        color="burnout_level"
    )
    st.plotly_chart(fig, use_container_width=True)

# ==============================
# TAB 4 — PREDICTION (UPDATED)
# ==============================
with tab4:

    st.subheader("Predict Burnout Risk")

    weekly_hours = st.slider("Weekly Hours", 20, 80)
    deliveries = st.slider("Deliveries per Week", 10, 150)
    income = st.slider("Weekly Income", 100, 2000)
    variability = st.slider("Income Variability", 0.0, 1.0)
    stress = st.slider("Stress Level", 1, 10)
    wlb = st.slider("Work-Life Balance", 1, 10)
    satisfaction = st.slider("Job Satisfaction", 1, 10)
    experience = st.slider("Experience (Years)", 0, 10)

    if st.button("Predict"):

        payload = {
            "weekly_hours": weekly_hours,
            "deliveries_per_week": deliveries,
            "weekly_income": income,
            "income_variability": variability,
            "stress_level": stress,
            "work_life_balance": wlb,
            "job_satisfaction": satisfaction,
            "experience_years": experience
        }

        try:
            result = predict(payload)

            # ==============================
            # RESULT DISPLAY
            # ==============================
            if result == 1:
                st.error("🔥 High Burnout Risk")
            else:
                st.success("✅ Low Burnout Risk")

            # ==============================
            # RECOMMENDATIONS
            # ==============================
            st.markdown("### 💡 Recommendations")

            rec = []

            if stress > 7:
                rec.append("Reduce workload and manage stress")

            if weekly_hours > 55:
                rec.append("Limit working hours")

            if variability > 0.5:
                rec.append("Stabilize income")

            if wlb < 5:
                rec.append("Improve work-life balance")

            if satisfaction < 5:
                rec.append("Improve job satisfaction")

            if len(rec) == 0:
                rec.append("Maintain current work pattern")

            for r in rec:
                st.write(f"• {r}")

        except Exception as e:
            st.error(f"Prediction Error: {e}")

# ==============================
# TAB 5 — SEGMENTATION
# ==============================
with tab5:
    fig = px.scatter(
        df,
        x="total_orders",
        y="burnout_score",
        color="cluster",
        hover_data=["rider_id"]
    )
    st.plotly_chart(fig, use_container_width=True)

# ==============================
# ALERTS
# ==============================
st.subheader("🚨 High Risk Riders")

high_risk = df[df["burnout_level"] == "High"]

if len(high_risk) > 0:
    st.dataframe(high_risk[["rider_id", "burnout_score", "workload_index"]])
else:
    st.info("No high-risk riders detected")

# ==============================
# GLOBAL RECOMMENDATION
# ==============================
st.subheader("💡 System Recommendation")

if len(high_risk) > 0:
    st.warning("""
    ⚠️ High burnout risk detected across workforce

    Suggested Actions:
    - Reduce workload
    - Limit night shifts
    - Balance order allocation
    - Encourage rest periods
    """)
else:
    st.success("✅ Workforce is stable")

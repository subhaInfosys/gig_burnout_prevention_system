import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="WIBPS Dashboard", layout="wide")

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
# APPLY FILTERS (FOR CHARTS ONLY)
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
    st.subheader("Workload vs Burnout")

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
# TAB 2 — BURNOUT ANALYSIS
# ==============================
with tab2:
    st.subheader("Burnout Distribution")

    fig = px.box(
        filtered_df,
        x="burnout_level",
        y="burnout_score",
        color="burnout_level"
    )
    st.plotly_chart(fig, use_container_width=True)

# ==============================
# TAB 3 — WORKLOAD INSIGHTS
# ==============================
with tab3:
    st.subheader("Order Value vs Burnout")

    fig = px.scatter(
        filtered_df,
        x="avg_order_value",
        y="burnout_score",
        color="burnout_level"
    )
    st.plotly_chart(fig, use_container_width=True)

# ==============================
# TAB 4 — API PREDICTION
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
            res = requests.post("http://localhost:8000/predict", json=payload)

            if res.status_code == 200:
                result = res.json()

                if result["label"] == "High":
                    st.error("🔥 High Burnout Risk")
                else:
                    st.success("✅ Low Burnout Risk")

            else:
                st.error("API Error: " + res.text)

        except:
            st.error("⚠️ API not running. Start backend first.")

# ==============================
# TAB 5 — SEGMENTATION
# ==============================
with tab5:
    st.subheader("Worker Segmentation")

    fig = px.scatter(
        df,
        x="total_orders",
        y="burnout_score",
        color="cluster",
        hover_data=["rider_id"]
    )
    st.plotly_chart(fig, use_container_width=True)

# ==============================
# ALERTS SECTION (FIXED + BONUS)
# ==============================
st.subheader("🚨 High Risk Riders")
st.caption("Showing high-risk riders across entire workforce")

high_risk = df[df["burnout_level"] == "High"]

if len(high_risk) > 0:
    st.dataframe(high_risk[["rider_id", "burnout_score", "workload_index"]])
else:
    st.info("No high-risk riders detected")

# ==============================
# RECOMMENDATIONS
# ==============================
st.subheader("💡 Recommendations")

if len(high_risk) > 0:
    st.warning("⚠️ High burnout risk detected")

    st.write("""
    Suggested Actions:
    - Reduce workload for high-risk riders
    - Limit night shift assignments
    - Balance order distribution
    - Encourage rest periods
    """)
else:
    st.success("✅ Workforce is stable")

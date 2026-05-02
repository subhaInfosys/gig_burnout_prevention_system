import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import sys
import os
from sklearn.cluster import KMeans

# ==============================
# FIX IMPORT PATH
# ==============================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="Courier Burnout Intelligence", layout="wide")

# ==============================
# LOAD DATA
# ==============================
df = pd.read_csv("data/courier_data.csv")

# ==============================
# CREATE TARGET
# ==============================
df["burnout_risk"] = (
    (df["stress_level"] > 7) &
    (df["weekly_hours"] > 55) &
    (df["income_variability"] > 0.4)
).astype(int)

# ==============================
# CLUSTERING (FOR FIGURE D4)
# ==============================
cluster_features = df[["weekly_hours", "stress_level", "income_variability"]]
kmeans = KMeans(n_clusters=3, random_state=42)
df["cluster"] = kmeans.fit_predict(cluster_features)

# ==============================
# API CONFIG
# ==============================
API_URL = "http://localhost:8000/predict"

# ==============================
# SIDEBAR FILTERS
# ==============================
st.sidebar.header("🔎 Filters")

hours_range = st.sidebar.slider("Weekly Hours", 20, 80, (20, 80))
stress_range = st.sidebar.slider("Stress Level", 1, 10, (1, 10))
income_range = st.sidebar.slider("Weekly Income", 100, 2000, (100, 2000))
wlb_range = st.sidebar.slider("Work-Life Balance", 1, 10, (1, 10))

burnout_filter = st.sidebar.selectbox(
    "Burnout Risk",
    ["All", "Low", "High"]
)

# ==============================
# APPLY FILTERS
# ==============================
filtered_df = df[
    (df["weekly_hours"].between(*hours_range)) &
    (df["stress_level"].between(*stress_range)) &
    (df["weekly_income"].between(*income_range)) &
    (df["work_life_balance"].between(*wlb_range))
]

if burnout_filter == "Low":
    filtered_df = filtered_df[filtered_df["burnout_risk"] == 0]
elif burnout_filter == "High":
    filtered_df = filtered_df[filtered_df["burnout_risk"] == 1]

# ==============================
# HEADER
# ==============================
st.title("🚴 Courier Burnout Intelligence Dashboard")
st.markdown("### Work Stability and Burnout Risk Analysis (ML System)")
st.markdown("---")

# ==============================
# KPI SECTION
# ==============================
col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Couriers", len(filtered_df))
col2.metric("⏱ Avg Hours", round(filtered_df["weekly_hours"].mean(), 1))
col3.metric("😰 Avg Stress", round(filtered_df["stress_level"].mean(), 1))
col4.metric("🔥 Burnout Rate", f"{round(filtered_df['burnout_risk'].mean()*100, 2)}%")

# ==============================
# TABS (NEW TAB ADDED)
# ==============================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "🔥 Burnout Analysis",
    "💰 Income Insights",
    "🎯 Prediction & Recommendation",
    "📈 Research Figures"
])

# ==============================
# TAB 1 — OVERVIEW
# ==============================
with tab1:
    fig = px.scatter(
        filtered_df,
        x="weekly_hours",
        y="stress_level",
        color="burnout_risk",
        size="weekly_income",
        color_continuous_scale="RdYlGn_r"
    )
    st.plotly_chart(fig, use_container_width=True)

# ==============================
# TAB 2 — BURNOUT
# ==============================
with tab2:
    fig = px.box(
        filtered_df,
        x="burnout_risk",
        y="stress_level",
        color="burnout_risk"
    )
    st.plotly_chart(fig, use_container_width=True)

# ==============================
# TAB 3 — INCOME
# ==============================
with tab3:
    fig = px.scatter(
        filtered_df,
        x="weekly_income",
        y="income_variability",
        color="burnout_risk"
    )
    st.plotly_chart(fig, use_container_width=True)

# ==============================
# TAB 4 — PREDICTION
# ==============================
with tab4:

    hours = st.slider("Weekly Hours", 20, 80)
    stress = st.slider("Stress Level", 1, 10)
    deliveries = st.slider("Deliveries per Week", 10, 150)
    income = st.slider("Weekly Income", 100, 2000)
    variability = st.slider("Income Variability", 0.0, 1.0)
    wlb = st.slider("Work-Life Balance", 1, 10)
    satisfaction = st.slider("Job Satisfaction", 1, 10)
    experience = st.slider("Experience (Years)", 0, 10)

    if st.button("Predict"):

        payload = {
            "weekly_hours": int(hours),
            "deliveries_per_week": int(deliveries),
            "weekly_income": int(income),
            "income_variability": float(variability),
            "stress_level": int(stress),
            "work_life_balance": int(wlb),
            "job_satisfaction": int(satisfaction),
            "experience_years": int(experience)
        }

        try:
            res = requests.post(API_URL, json=payload)

            if res.status_code == 200:
                result = res.json()

                if result["label"] == "High":
                    st.error("🔥 High Burnout Risk")
                else:
                    st.success("✅ Low Burnout Risk")

            else:
                st.error(res.text)

        except:
            st.error("API not running")

# ==============================
# TAB 5 — RESEARCH FIGURES (NEW)
# ==============================
with tab5:

    st.subheader("📊 Figure D1: Burnout Distribution")
    fig1 = px.histogram(
        df,
        x="burnout_risk",
        color="burnout_risk",
        color_discrete_sequence=["#00cc96", "#EF553B"]
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("📊 Figure D2: Hours vs Burnout")
    fig2 = px.box(
        df,
        x="burnout_risk",
        y="weekly_hours",
        color="burnout_risk"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📊 Figure D3: Income Variability Impact")
    fig3 = px.scatter(
        df,
        x="income_variability",
        y="stress_level",
        color="burnout_risk",
        color_continuous_scale="Turbo"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("📊 Figure D4: Courier Segmentation (Clustering)")
    fig4 = px.scatter(
        df,
        x="weekly_hours",
        y="stress_level",
        color="cluster",
        title="Cluster Groups"
    )
    st.plotly_chart(fig4, use_container_width=True)

# 🚀 Courier Burnout Intelligence System

An end-to-end **Machine Learning + Analytics + API + Interactive Dashboard** system designed to analyze and predict burnout risk among gig economy food delivery couriers.

This project addresses a key gap in the gig economy:
👉 **lack of data-driven visibility into workforce stress, instability, and burnout risk**, which leads to poor decision-making and reduced worker well-being.

---

# 📌 Problem Statement

The gig economy offers flexibility but often results in:

* ❌ Unstable income
* ❌ Long and irregular working hours
* ❌ High stress levels
* ❌ Poor work-life balance

Currently, there is **no structured system to identify burnout risk early**.

👉 This project solves that by providing a **data-driven burnout prediction and decision-support system**.

---

# 🎯 What This System Does

* Predicts **burnout risk (High / Low)**
* Analyzes **key drivers of burnout**
* Segments workers using **clustering**
* Provides **actionable recommendations**
* Visualizes insights through an **interactive dashboard**

---

# 📊 Features

### 🔍 Analytics & Visualization

* Interactive Streamlit dashboard
* KPI metrics (stress, hours, burnout rate)
* Multi-tab insights (workload, income, burnout)

### 🤖 Machine Learning

* Logistic Regression
* Random Forest (best-performing model)
* Feature engineering (workload, stress ratio)

### 📡 Backend API

* FastAPI-based prediction service
* Real-time inference from dashboard

### 🎯 Decision Intelligence

* Burnout risk prediction
* Rule-based recommendation system
* Workforce segmentation (KMeans clustering)

### 📈 Research Figures (Thesis Ready)

* Burnout distribution
* Hours vs burnout
* Income variability impact
* Courier clustering

---

# 🧱 Project Structure

```
gig_burnout_project/
│
├── data/
│   └── courier_data.csv
│
├── ml/
│   ├── train.py
│   ├── preprocessing.py
│   ├── models.py
│   └── __init__.py
│
├── backend/
│   ├── api.py
│   ├── model_service.py
│   └── __init__.py
│
├── frontend/
│   ├── dashboard.py
│   └── __init__.py
│
├── artifacts/
│   ├── model.pkl
│   ├── scaler.pkl
│   └── features.pkl
│
├── requirements.txt
└── README.md
```

---

# ⚙️ Setup Instructions (Step-by-Step)

## 1️⃣ Clone the Project

```bash
git clone <your-repo-link>
cd gig_burnout_project
```

---

## 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ (Mac Only) Fix XGBoost Issue

```bash
brew install libomp
```

If needed:

```bash
sudo xcodebuild -license accept
```

---

## 5️⃣ Train the Model

```bash
python -m ml.train
```

✅ This generates:

```
artifacts/
├── model.pkl
├── scaler.pkl
├── features.pkl
```

---

## 6️⃣ Run Backend API

```bash
uvicorn backend.api:app --reload
```

👉 Open:

```
http://127.0.0.1:8000/docs
```

---

## 7️⃣ Run Dashboard

Open a new terminal:

```bash
streamlit run frontend/dashboard.py
```

👉 Dashboard:

```
http://localhost:8501
```

---

# 🧠 How the System Works

1. User inputs courier data via dashboard
2. Data sent to FastAPI backend
3. Backend:

   * Applies feature engineering
   * Aligns feature columns
   * Scales data
4. ML model predicts burnout risk
5. Dashboard displays:

   * Prediction
   * Insights
   * Recommendations

---

# 🔍 Burnout Logic (Core Idea)

Burnout risk is derived from:

* High stress level
* Long working hours
* High income variability

```python
burnout_risk = (
    (stress_level > 7) &
    (weekly_hours > 55) &
    (income_variability > 0.4)
)
```

---

# 📊 Key Insights

* 🔥 Stress level is the strongest predictor of burnout
* ⏱ Long working hours significantly increase risk
* 💸 Income instability contributes to burnout
* 📊 Cluster analysis reveals distinct workforce segments

---

# 🎯 Example Prediction Input

```json
{
  "weekly_hours": 60,
  "deliveries_per_week": 120,
  "weekly_income": 900,
  "income_variability": 0.7,
  "stress_level": 8,
  "work_life_balance": 3,
  "job_satisfaction": 4,
  "experience_years": 2
}
```

---

# ⚠️ Common Errors & Fixes

## ❌ ModuleNotFoundError

✔ Run with:

```bash
python -m ml.train
```

---

## ❌ API not responding

✔ Start backend:

```bash
uvicorn backend.api:app --reload
```

---

## ❌ Burnout always 0

✔ Ensure burnout logic exists in dashboard & preprocessing

---

## ❌ XGBoost error (Mac)

✔ Install:

```bash
brew install libomp
```

---

# 🚀 How to Use

1. Apply filters (sidebar)
2. Explore insights (tabs)
3. Go to **Prediction tab**
4. Enter courier details
5. Click **Predict**
6. View:

   * Burnout risk
   * Recommended actions

---

# 🎓 Academic Value

This project demonstrates:

* End-to-end ML pipeline
* Feature engineering & preprocessing
* Classification + clustering
* API-based deployment
* Interactive BI dashboard
* Decision-support system design

---

# 🧠 Contribution

This is not just a prediction model.

👉 It is a **Decision Intelligence System** that helps:

* Platforms optimize workforce management
* Reduce burnout risk
* Improve operational efficiency

---

# 👨‍💻 Author

Your Name
Business Intelligence / Data Science Project

---

# ⭐ Final Note

This system transforms raw gig worker data into **actionable insights**, enabling smarter, data-driven decisions in the gig economy.

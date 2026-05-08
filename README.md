# 🚀 Workforce Insight & Burnout Prevention System (WIBPS)

WIBPS is an end-to-end **SaaS-style workforce analytics system** designed to monitor, analyze, and predict burnout risk among **gig economy food delivery workers** (e.g., Uber Eats, Wolt, Lieferando).

The system integrates **data processing, machine learning, API services, and an interactive dashboard** to provide real-time decision support for workforce management.

---

# 📌 Problem Context

Gig workers operate in highly dynamic environments characterized by:

* Irregular working hours
* Fluctuating income
* High operational pressure
* Limited organizational support

Most existing tools focus on **employee surveys or well-being tracking**, which provide delayed or subjective insights.

👉 WIBPS addresses this gap by analyzing **behavioral and operational data** to estimate burnout risk and support proactive decision-making.

---

# 🎯 System Objective

The objective of WIBPS is to:

* Detect early signs of burnout risk
* Provide data-driven workforce insights
* Support operational decision-making
* Improve worker well-being and platform efficiency

---

# ⚙️ What WIBPS Does

### 🔍 Workforce Analytics

* Aggregates delivery activity into worker-level metrics
* Computes workload indicators (orders, night shifts, delivery time)

### 🤖 Burnout Risk Modeling

* Classifies workers into:

  * Low risk
  * Medium risk
  * High risk

### 🧠 Worker Segmentation

* Uses clustering (KMeans) to identify behavioral workforce groups

### 📊 Decision Dashboard

* Visualizes burnout patterns and workload distribution
* Highlights high-risk workers
* Provides actionable recommendations

### 📡 API-Based Prediction

* FastAPI backend enables real-time prediction requests
* Supports integration with external systems

---

# 🧠 Important Clarification

Burnout is influenced by multiple factors including:

* Personal life conditions
* Mental and physical health
* Financial and social stress

👉 WIBPS does **not diagnose burnout**, but estimates **operational burnout risk** based on observable work patterns.

---

# 🧱 System Architecture

```
Raw Data → Preprocessing → Feature Engineering → ML Model → API → Dashboard
```

---

# 📁 Project Structure

```
gig_burnout_prevention_system/
│
├── data/
│   ├── raw datasets
│   ├── processed_data.csv
│   └── model_output.csv
│
├── ml/
│   ├── data_preprocessing.py
│   ├── eda_analysis.py
│   └── model.py
│
├── backend/
│   ├── api.py
│   └── model_service.py
│
├── dashboard/
│   └── dashboard.py
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

# ⚙️ Setup Instructions

## 1️⃣ Clone Repository

```bash
git clone <your-repo-link>
cd gig_burnout_prevention_system
```

---

## 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Run Data Pipeline

```bash
python ml/data_preprocessing.py
```

Output:

```
data/processed_data.csv
data/attrition_cleaned.csv
```

---

## 5️⃣ Run Machine Learning Model

```bash
python ml/model.py
```

Output:

```
data/model_output.csv
```

---

## 6️⃣ Run Backend API

```bash
uvicorn backend.api:app --reload
```

API Docs:

```
http://127.0.0.1:8000/docs
```

---

## 7️⃣ Run Dashboard

```bash
streamlit run dashboard/dashboard.py
```

Dashboard:

```
http://localhost:8501
```

---

# 📊 Key Features

### ✔ Burnout Risk Classification

* Random Forest model
* Categorizes workers into Low / Medium / High risk

### ✔ Feature Engineering

* Workload index
* Night shift intensity
* Delivery efficiency

### ✔ Clustering

* KMeans segmentation
* Identifies high-pressure worker groups

### ✔ Dashboard Insights

* Workload vs burnout visualization
* Burnout distribution
* Worker segmentation
* High-risk alerts

---

# 📈 Example Insight

* High workload combined with night shifts increases burnout risk
* Not all high-hour workers are high-risk → workload composition matters
* Worker clusters reveal different behavioral patterns

---

# 🚨 Decision Support Output

The system enables managers to:

* Identify high-risk workers
* Adjust workload distribution
* Limit excessive night shifts
* Improve workforce stability

---

# ⚠️ Limitations

* Does not capture personal or psychological factors
* Uses simulated / public datasets
* Requires real platform data for production deployment

---

# 🎓 Academic Contribution

This project demonstrates:

* End-to-end ETL pipeline
* Exploratory Data Analysis (EDA)
* Supervised (classification) and unsupervised (clustering) ML
* API-based deployment
* Interactive BI dashboard
* Decision-support system design

---

# 👨‍💻 Author

Subhendu Kumar Pati
Business Intelligence Project

---

# ⭐ Final Note

WIBPS transforms operational gig worker data into **actionable workforce intelligence**, enabling platforms to shift from reactive management to **proactive burnout prevention**.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
df = pd.read_csv('data/processed_data.csv')
attrition = pd.read_csv('data/attrition_cleaned.csv')

# -----------------------------
# 1. DATA OVERVIEW
# -----------------------------
print("\n📊 DATA SUMMARY (Gig Workers):")
print(df.describe())

print("\n📊 DATA SUMMARY (Attrition):")
print(attrition.describe())


# -----------------------------
# 2. BOXPLOT (OUTLIERS)
# -----------------------------
plt.figure()
df[['avg_delivery_time', 'total_orders', 'burnout_score']].boxplot()
plt.title("Boxplot - Gig Worker Metrics")
plt.show()


# -----------------------------
# 3. CATEGORICAL VISUALIZATION
# -----------------------------
if 'Department' in attrition.columns:
    attrition['Department'].value_counts().plot(kind='bar')
    plt.title("Employee Distribution by Department")
    plt.show()


# -----------------------------
# 4. SALARY / INCOME ANALYSIS
# -----------------------------
if 'MonthlyIncome' in attrition.columns:
    plt.figure()
    sns.histplot(attrition['MonthlyIncome'], kde=True)
    plt.title("Income Distribution")
    plt.show()


# -----------------------------
# 5. CORRELATION ANALYSIS
# -----------------------------
plt.figure()
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
plt.title("Correlation Matrix - Gig Workers")
plt.show()


# -----------------------------
# 6. WORKLOAD VS BURNOUT
# -----------------------------
plt.figure()
sns.scatterplot(x=df['workload_index'], y=df['burnout_score'])
plt.title("Workload vs Burnout")
plt.show()


# -----------------------------
# 7. NIGHT WORK IMPACT
# -----------------------------
plt.figure()
sns.scatterplot(x=df['night_orders'], y=df['burnout_score'])
plt.title("Night Work vs Burnout")
plt.show()


# -----------------------------
# 8. ADDITIONAL INSIGHTS
# -----------------------------
print("\n🔍 Interesting Insights:")

print("Correlation with Burnout:")
print(df.corr(numeric_only=True)['burnout_score'].sort_values(ascending=False))

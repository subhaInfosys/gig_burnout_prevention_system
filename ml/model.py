import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv('data/processed_data.csv')

# -----------------------------
# CREATE TARGET CLASSES
# -----------------------------
def categorize_burnout(score):
    if score < 40:
        return "Low"
    elif score < 70:
        return "Medium"
    else:
        return "High"

df['burnout_level'] = df['burnout_score'].apply(categorize_burnout)

# -----------------------------
# FEATURES & TARGET
# -----------------------------
features = [
    'avg_delivery_time',
    'total_orders',
    'night_orders',
    'weekend_orders',
    'workload_index',
    'avg_order_value'
]

X = df[features]
y = df['burnout_level']

# -----------------------------
# TRAIN TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# CLASSIFICATION MODEL
# -----------------------------
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

print("\n📊 CLASSIFICATION RESULTS:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# -----------------------------
# FEATURE IMPORTANCE
# -----------------------------
importances = model.feature_importances_

print("\n🔍 FEATURE IMPORTANCE:")
for f, imp in zip(features, importances):
    print(f"{f}: {round(imp, 3)}")

# -----------------------------
# CLUSTERING (UNSUPERVISED)
# -----------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(X_scaled)

print("\n📊 CLUSTER DISTRIBUTION:")
print(df['cluster'].value_counts())

# Save output
df.to_csv('data/model_output.csv', index=False)

print("\n✅ Model output saved → data/model_output.csv")

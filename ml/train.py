import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from ml.preprocessing import load_data, preprocess
from ml.model import get_models

df = load_data()

X, y, scaler, feature_names = preprocess(df)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

models = get_models()

best_model = None
best_score = 0

for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    score = accuracy_score(y_test, preds)
    print(f"{name}: {score}")

    if score > best_score:
        best_score = score
        best_model = model

# Save artifacts
joblib.dump(best_model, "artifacts/model.pkl")
joblib.dump(scaler, "artifacts/scaler.pkl")
joblib.dump(feature_names.tolist(), "artifacts/features.pkl")

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# ==============================
# MODEL DEFINITIONS
# ==============================
def get_models():
    """
    Returns a dictionary of models to train and compare.
    """

    models = {
        "logistic_regression": LogisticRegression(
            max_iter=1000,
            solver="lbfgs"
        ),

        "random_forest": RandomForestClassifier(
            n_estimators=100,
            max_depth=None,
            random_state=42
        )
    }

    return models

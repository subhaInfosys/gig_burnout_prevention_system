from fastapi import FastAPI
from backend.model_service import predict

app = FastAPI()


@app.get("/")
def home():
    return {"status": "API running"}


@app.post("/predict")
def get_prediction(data: dict):
    result = predict(data)

    return {
        "burnout_risk": result,
        "label": "High" if result == 1 else "Low"
    }


# ==============================
# LOCAL RUN OPTION
# ==============================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.api:app", host="0.0.0.0", port=8000, reload=True)

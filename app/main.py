
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from sklearn.ensemble import IsolationForest
import os
import pandas as pd

app = FastAPI(title="CloudPulse")

UPLOAD_FOLDER = "uploads"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "CloudPulse",
        "environment": ENVIRONMENT
    }


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = os.path.basename(file.filename or "upload.csv")
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "message": "File uploaded successfully",
        "filename": filename
    }


@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    if "score" not in df.columns:
        return {
            "error": "CSV must contain a 'score' column"
        }

    scores = pd.to_numeric(df["score"], errors="coerce").dropna()

    if scores.empty:
        return {
            "error": "CSV must contain numeric scores"
        }

    return {
        "rows": len(scores),
        "average_score": round(scores.mean(), 2),
        "highest_score": float(scores.max()),
        "lowest_score": float(scores.min())
    }



@app.post("/detect-anomalies")
async def detect_anomalies(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid CSV file"}
        )

    if "score" not in df.columns:
        return JSONResponse(
            status_code=400,
            content={"error": "CSV must contain a 'score' column"}
        )

    scores = pd.to_numeric(df["score"], errors="coerce").dropna()

    if len(scores) < 5:
        return JSONResponse(
            status_code=400,
            content={"error": "At least 5 numeric scores are required"}
        )

    model = IsolationForest(
        n_estimators=100,
        contamination="auto",
        random_state=42
    )

    predictions = model.fit_predict(scores.to_numpy().reshape(-1, 1))

    anomalies = [
        {
            "row": int(index) + 1,
            "score": float(score)
        }
        for index, score, prediction in zip(
            scores.index, scores.values, predictions
        )
        if prediction == -1
    ]

    return {
        "application": "CloudPulse",
        "model": "IsolationForest",
        "rows_analyzed": len(scores),
        "anomalies_detected": len(anomalies),
        "anomalies": anomalies
    }

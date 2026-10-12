from fastapi import FastAPI, UploadFile, File
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
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "message": "File uploaded successfully",
        "filename": file.filename
    }


@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    if "score" not in df.columns:
        return {
            "error": "CSV must contain a 'score' column"
        }

    return {
        "rows": len(df),
        "average_score": round(df["score"].mean(), 2),
        "highest_score": int(df["score"].max()),
        "lowest_score": int(df["score"].min())
    }

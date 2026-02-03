from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import sqlite3
import datetime
from typing import Optional

# ======================================================
# Database Configuration
# ======================================================

DB_PATH = "feedback.db"

def get_db_connection():
    """
    Creates a new database connection per request.
    This avoids race conditions and SQLite locking issues.
    """
    return sqlite3.connect(DB_PATH)

def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            timestamp TEXT,
            income REAL,
            loan_amount REAL,
            credit_history INTEGER,
            prediction INTEGER,
            actual INTEGER
        )
    """)
    conn.commit()
    conn.close()

initialize_database()

# ======================================================
# FastAPI App Initialization
# ======================================================

app = FastAPI(
    title="Self-Correcting Loan Engine",
    version="1.0"
)

# ======================================================
# Load Model
# ======================================================

MODEL_PATH = "artifacts/model.pkl"

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")

# ======================================================
# Schemas
# ======================================================

class LoanApplication(BaseModel):
    Income: float = Field(..., gt=0)
    LoanAmount: float = Field(..., gt=0)
    CreditHistory: int = Field(..., ge=0, le=1)

class Feedback(BaseModel):
    Income: float
    LoanAmount: float
    CreditHistory: int
    prediction: int
    actual: int

# ======================================================
# Prediction Endpoint
# ======================================================

@app.post("/predict")
def predict_loan(data: LoanApplication):
    try:
        df = pd.DataFrame([data.dict()])
        prediction = int(model.predict(df)[0])

        # Defensive probability handling
        if hasattr(model, "predict_proba"):
            probability = float(model.predict_proba(df)[0][1])
        else:
            probability = None

        return {
            "prediction": prediction,
            "probability": probability
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ======================================================
# Feedback Endpoint (Human-in-the-Loop)
# ======================================================

@app.post("/feedback")
def log_feedback(data: Feedback):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO feedback VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.datetime.utcnow().isoformat(),
                data.Income,
                data.LoanAmount,
                data.CreditHistory,
                data.prediction,
                data.actual
            )
        )
        conn.commit()

        return {"message": "Feedback Logged Successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        conn.close()

# ======================================================
# Monitoring / Stats Endpoint
# ======================================================

@app.get("/stats")
def get_stats():
    conn = get_db_connection()

    try:
        df = pd.read_sql("SELECT * FROM feedback", conn)

        if df.empty:
            return {
                "total_feedback": 0,
                "live_accuracy": None
            }

        correct = (df["prediction"] == df["actual"]).sum()
        total = len(df)

        return {
            "total_feedback": total,
            "live_accuracy": round(correct / total, 3)
        }

    finally:
        conn.close()
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib 
import pandas as pd 

# Adding SQlite3 Setup

import sqlite3
import datetime

# initializing the Database 

DB_PATH = "Feedback.db"

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
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

# Initialize the app

app = FastAPI(
    title = "Self - Correcting Loan Engine",
    version = "1.0"
)

# Loading the model 

MODEL_PATH = "artifacts/model.pkl"

try:
    model = joblib.load(MODEL_PATH)
except Exception as e: 
    raise RuntimeError(f"Failed to Load the Model: {e}")

# Define the Input Schema 

class LoanApplication(BaseModel):
    Income: float = Field(..., gt = 0)
    LoanAmount: float = Field(..., gt = 0)
    CreditHistory: int = Field(..., ge = 0, le = 1)

# Defining Feedback Schema 

class Feedback(BaseModel):
    Income : float 
    LoanAmount : float 
    CreditHistory : int 
    prediction : int 
    actual : int 

@app.post("/predict")
def predict_loan(data: LoanApplication):
    try:
        df = pd.DataFrame([data.dict()])
        prediction = int(model.predict(df)[0])
        probability = float(model.predict_proba(df)[0][1])


        return {
            "prediction" : prediction, 
            "probability" : probability
        }

    except Exception as e:
        raise HTTPException(status_code= 500, detail = str(e))



# Adding Feedback endPoint 
@app.post("/feedback")
def log_feedback(data: Feedback):
    try:
        cursor.execute(
            """
            INSERT INTO feedback
            VALUES (?, ?, ?, ?, ?, ?)
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


        return {
            "message" : "Feedback Logged Successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Adding Monitoring EndPoint 

@app.get("/stats")
def get_stats():
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
        "live_accuracy": round(correct / total, 3) if total > 0 else None
    }
    

 
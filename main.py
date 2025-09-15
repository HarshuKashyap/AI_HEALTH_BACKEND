# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import ai_logic
import db
import datetime

app = FastAPI(title="AI Healthcare Assistant Backend")

# Dev CORS - in production restrict origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SymptomRequest(BaseModel):
    symptoms: str
    user_id: Optional[str] = None

class PredictResponse(BaseModel):
    advice: str
    probable_conditions: List[str]
    severity: str
    recommendations: List[str]

@app.on_event("startup")
def startup_event():
    db.init_db()

@app.get("/")
def read_root():
    return {"message": "AI Healthcare Assistant Backend is running 🚀", "time": datetime.datetime.utcnow().isoformat()}

@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.datetime.utcnow().isoformat()}

@app.post("/predict", response_model=PredictResponse)
def predict(req: SymptomRequest):
    if not req.symptoms or len(req.symptoms.strip()) < 3:
        raise HTTPException(status_code=400, detail="Provide a short description of symptoms.")
    result = ai_logic.analyze_symptoms(req.symptoms)
    db.save_query(req.symptoms, result)
    return {
        "advice": result["advice"],
        "probable_conditions": result["probable_conditions"],
        "severity": result["severity"],
        "recommendations": result["recommendations"]
    }

@app.get("/history")
def history(limit: int = 20):
    return db.get_history(limit)

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.agents.treatment_agent import TreatmentAgent

router = APIRouter()
agent = TreatmentAgent()

class PatientData(BaseModel):
    age: int
    weight: float
    condition: str
    history: Optional[str] = None
    current_meds: Optional[List[str]] = []
    allergies: Optional[List[str]] = []

@router.post("/recommend-treatment")
async def recommend_treatment(data: PatientData):
    try:
        recommendation = agent.recommend_treatment(data.dict())
        return {"recommendation": recommendation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

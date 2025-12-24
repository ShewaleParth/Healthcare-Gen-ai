from fastapi import APIRouter
from app.schemas.patient import Patient
from app.agents.treatment_agent import recommend_treatment

router = APIRouter()

@router.post("/treatment")
def treatment_recommendation(patient: Patient):
    result = recommend_treatment(patient.dict())
    return {
        "status": "success",
        "treatment_plan": result
    }

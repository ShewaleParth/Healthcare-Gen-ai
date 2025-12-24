from fastapi import APIRouter, HTTPException
from app.schemas.patient import Patient
from app.agents.treatment_agent import TreatmentAgent

router = APIRouter()

# Initialize the treatment agent
treatment_agent = TreatmentAgent()

@router.post("/recommend")
def treatment_recommendation(patient: Patient):
    """Generate treatment recommendation based on patient data"""
    try:
        # Convert patient data to dict
        patient_data = patient.dict()
        
        # Get treatment recommendation
        result = treatment_agent.recommend_treatment(patient_data)
        
        return {
            "status": "success",
            "recommendation": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Treatment recommendation failed: {str(e)}")

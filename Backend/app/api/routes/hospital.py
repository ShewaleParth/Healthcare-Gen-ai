from fastapi import APIRouter, HTTPException
from app.agents.hospital_agent import HospitalAgent

router = APIRouter()
agent = HospitalAgent()

@router.post("/optimize")
async def optimize_hospital():
    try:
        result = agent.analyze_situation()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

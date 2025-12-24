from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agents.mental_health_agent import MentalHealthAgent

router = APIRouter()
agent = MentalHealthAgent()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = agent.chat(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

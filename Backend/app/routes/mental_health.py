from fastapi import APIRouter
from app.agents.mental_agent import run_mental_health_agent

router = APIRouter()

@router.post("/mental-health/chat")
def mental_health_chat(payload: dict):
    user_message = payload.get("message", "")
    result = run_mental_health_agent(user_message)

    return {
        "status": "success",
        "ai_response": result
    }

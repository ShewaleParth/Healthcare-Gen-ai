from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.agents.mental_health_agent import MentalHealthAgent

router = APIRouter()

# Initialize the mental health agent
mental_health_agent = MentalHealthAgent()

class ChatMessage(BaseModel):
    message: str
    history: Optional[List[dict]] = None

@router.post("/chat")
def mental_health_chat(payload: ChatMessage):
    """Chat with mental health AI companion"""
    try:
        # Get user message and history
        user_message = payload.message
        history = payload.history or []
        
        # Get AI response with risk assessment
        result = mental_health_agent.chat(user_message, history)
        
        return {
            "status": "success",
            "response": result["response"],
            "risk_level": result["risk_level"],
            "emergency_protocol": result.get("emergency_protocol", False)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mental health chat failed: {str(e)}")

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.agents.user_health_agent import UserHealthAgent

router = APIRouter()
agent = UserHealthAgent()

class UserHealthRequest(BaseModel):
    user_id: Optional[str] = "USER001"
    date_range: Optional[str] = "30d"  # 7d, 30d, 90d, 1y

@router.post("/dashboard")
async def get_user_health_dashboard(request: UserHealthRequest):
    """
    Get comprehensive health dashboard data for a specific user.
    Returns personalized health metrics, diagnostics, treatments, and AI insights.
    """
    try:
        # Generate user health data
        health_data = agent.generate_user_health_data(user_id=request.user_id)
        
        # Generate AI insights
        ai_insights = agent.generate_ai_insights(health_data)
        
        # Combine data with AI insights
        response = {
            **health_data,
            "ai_insights": ai_insights
        }
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/vitals/{user_id}")
async def get_user_vitals(user_id: str):
    """Get current vital signs for a user."""
    try:
        health_data = agent.generate_user_health_data(user_id=user_id)
        return {
            "user_id": user_id,
            "vitals": health_data["vitals"],
            "health_score": health_data["health_score"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/timeline/{user_id}")
async def get_user_timeline(user_id: str):
    """Get medical timeline for a user."""
    try:
        health_data = agent.generate_user_health_data(user_id=user_id)
        return {
            "user_id": user_id,
            "timeline": health_data["timeline"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

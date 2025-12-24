from fastapi import APIRouter, HTTPException
from app.agents.hospital_agent import HospitalAgent

router = APIRouter()

# Initialize the hospital agent
hospital_agent = HospitalAgent()

@router.get("/forecast")
def hospital_forecast():
    """Get patient load forecast for the next 7 days"""
    try:
        # Get simulated hospital data
        data = hospital_agent.simulate_hospital_data()
        
        return {
            "status": "success",
            "timestamp": data["timestamp"],
            "opd_visits": data["opd_visits"],
            "message": "Hospital forecast data generated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forecast generation failed: {str(e)}")

@router.post("/optimize")
def hospital_optimization():
    """Get hospital operations optimization recommendations"""
    try:
        # Get full optimization analysis
        result = hospital_agent.optimize_hospital_operations()
        
        if result["success"]:
            return {
                "status": "success",
                "analysis": result["analysis"],
                "raw_data": result["raw_data"]
            }
        else:
            return {
                "status": "error",
                "analysis": result["analysis"],
                "raw_data": result["raw_data"],
                "error": result.get("error", "Unknown error")
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")

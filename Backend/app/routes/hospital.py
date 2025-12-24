from fastapi import APIRouter
from app.agents.hospital_agent import predict_patient_load, optimize_hospital_ops

router = APIRouter(prefix="/hospital")

@router.get("/forecast")
def hospital_forecast():
    load = predict_patient_load()
    return {
        "status": "success",
        "next_7_days_patient_load": load
    }

@router.get("/optimize")
def hospital_optimization():
    load = predict_patient_load()
    optimization = optimize_hospital_ops(load)

    return {
        "status": "success",
        "forecast": load,
        "optimization_plan": optimization
    }

import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.agents.diagnostic_agent import DiagnosticAgent
from pathlib import Path

router = APIRouter()

# Initialize the diagnostic agent
diagnostic_agent = DiagnosticAgent()

UPLOAD_DIR = "uploads/medical_images"
HEATMAP_DIR = "uploads/heatmaps"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(HEATMAP_DIR, exist_ok=True)

@router.post("/diagnose")
async def diagnose_image(file: UploadFile = File(...)):
    """Analyze medical image using AI"""
    return await _analyze_image(file)

@router.post("/analyze-image")
async def analyze_image_alias(file: UploadFile = File(...)):
    """Alias for /diagnose endpoint (frontend compatibility)"""
    return await _analyze_image(file)

async def _analyze_image(file: UploadFile):
    """Internal function for image analysis"""
    try:
        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        # Run diagnostic analysis
        analysis = diagnostic_agent.analyze_image(file_path)
        
        return {
            "status": "success",
            "filename": file.filename,
            "analysis": analysis,
            "ml_used": False,  # Currently using text-based AI
            "heatmaps": []  # No heatmaps in current version
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diagnostic analysis failed: {str(e)}")


@router.get("/heatmap/{filename}")
async def get_heatmap(filename: str):
    """Serve generated heatmap images"""
    try:
        file_path = os.path.join(HEATMAP_DIR, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Heatmap not found")
        
        return FileResponse(file_path, media_type="image/png")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to serve heatmap: {str(e)}")

@router.get("/status")
def get_diagnostic_status():
    """Get diagnostic system status"""
    return {
        "status": "operational",
        "ml_available": False,
        "mode": "AI-based (Llama 3.3 70B Medical Expert)",
        "models": ["llama-3.3-70b-versatile"],
        "api_available": diagnostic_agent.groq_client is not None
    }

from fastapi import APIRouter, File, UploadFile, HTTPException
from app.agents.diagnostic_agent import DiagnosticAgent
import shutil
from pathlib import Path

router = APIRouter()
agent = DiagnosticAgent()

UPLOAD_DIR = Path("temp_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    try:
        file_location = UPLOAD_DIR / file.filename
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        analysis = agent.analyze_image(str(file_location))
        
        # Cleanup
        # file_location.unlink() 
        
        return {"filename": file.filename, "analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

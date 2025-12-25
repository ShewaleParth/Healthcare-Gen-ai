from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from app.agents.diagnostic_agent import DiagnosticAgent
import shutil
from pathlib import Path
from typing import Optional

router = APIRouter()
agent = DiagnosticAgent()

UPLOAD_DIR = Path("temp_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/analyze-image")
async def analyze_image(
    file: UploadFile = File(...),
    language: Optional[str] = Form("en")
):
    """
    Analyze medical image with multilingual support.
    
    Args:
        file: Medical image file
        language: Language code (en, hi, mr) for report generation
    """
    try:
        file_location = UPLOAD_DIR / file.filename
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        analysis = agent.analyze_image(str(file_location), language=language)
        
        # Cleanup
        # file_location.unlink() 
        
        return {"filename": file.filename, "analysis": analysis, "language": language}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


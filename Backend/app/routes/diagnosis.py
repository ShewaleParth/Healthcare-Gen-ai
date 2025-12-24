import os
from fastapi import APIRouter, UploadFile, File
from app.agents.diagnostic_agent import run_diagnostic

router = APIRouter()

UPLOAD_DIR = "uploads/medical_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/diagnose")
async def diagnose_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    result = run_diagnostic(file_path)

    return {
        "status": "success",
        "filename": file.filename,
        "result": result
    }

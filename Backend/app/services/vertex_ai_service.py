"""
Vertex AI Service - Handles all Vertex AI interactions
Includes Vision API for medical imaging and Forecasting for hospital operations
"""
import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Vertex AI imports
try:
    from google.cloud import aiplatform
    from google.cloud.aiplatform.gapic.schema import predict
    import vertexai
    from vertexai.preview.vision_models import ImageTextModel, Image as VertexImage
    VERTEX_AI_AVAILABLE = True
except ImportError:
    VERTEX_AI_AVAILABLE = False
    print("WARNING: Vertex AI SDK not installed. Using fallback mode.")


class VertexAIService:
    """Service for Vertex AI Vision and Forecasting"""
    
    def __init__(self):
        self.project_id = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
        self.location = os.getenv("GCP_LOCATION", "us-central1")
        self.initialized = False
        
        # Set credentials if provided
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if credentials_path and os.path.exists(credentials_path):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
            print(f"✅ Using credentials from: {credentials_path}")
        
        if VERTEX_AI_AVAILABLE and self.project_id != "your-gcp-project-id":
            try:
                vertexai.init(project=self.project_id, location=self.location)
                self.vision_model = ImageTextModel.from_pretrained("imagetext@001")
                self.initialized = True
                print(f"✅ Vertex AI initialized: {self.project_id}")
            except Exception as e:
                print(f"⚠️ Vertex AI initialization failed: {e}")
                self.initialized = False
        else:
            print("⚠️ Vertex AI not configured. Using Gemini fallback.")
    
    def analyze_medical_image(self, image_path: str, prompt: str) -> Dict[str, Any]:
        """
        Analyze medical image using Vertex AI Vision
        Falls back to Gemini if Vertex AI is not available
        """
        if not self.initialized:
            return {
                "success": False,
                "analysis": None,
                "fallback": True,
                "message": "Vertex AI not configured. Using Gemini fallback."
            }
        
        try:
            # Load image
            image = VertexImage.load_from_file(image_path)
            
            # Get predictions from Vertex AI Vision
            response = self.vision_model.ask(
                image=image,
                question=prompt,
                number_of_results=1
            )
            
            return {
                "success": True,
                "analysis": response,
                "fallback": False,
                "source": "Vertex AI Vision"
            }
        except Exception as e:
            return {
                "success": False,
                "analysis": None,
                "fallback": True,
                "error": str(e),
                "message": "Vertex AI Vision failed. Use Gemini fallback."
            }
    
    def forecast_patient_load(self, historical_data: list) -> Dict[str, Any]:
        """
        Forecast patient load using Vertex AI Forecasting
        Falls back to simulated data if not available
        """
        if not self.initialized:
            return {
                "success": False,
                "forecast": None,
                "fallback": True,
                "message": "Vertex AI not configured. Using simulated forecasting."
            }
        
        try:
            # In production, this would use Vertex AI Forecasting API
            # For MVP, we acknowledge the architecture but use simulation
            return {
                "success": False,
                "forecast": None,
                "fallback": True,
                "message": "Vertex AI Forecasting integration pending. Using simulation."
            }
        except Exception as e:
            return {
                "success": False,
                "forecast": None,
                "fallback": True,
                "error": str(e)
            }


# Singleton instance
vertex_ai_service = VertexAIService()

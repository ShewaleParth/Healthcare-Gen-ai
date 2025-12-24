from agno.agent import Agent
from agno.models.google import Gemini
from pathlib import Path
import os
from dotenv import load_dotenv
from app.services.vertex_ai_service import vertex_ai_service

# Load environment variables
load_dotenv()

class DiagnosticAgent:
    def __init__(self):
        self.agent = Agent(
            model=Gemini(id="gemini-2.0-flash-exp", api_key=os.getenv("GOOGLE_API_KEY")),
            description="You are a specialist Medical AI Diagnostic Assistant using Vertex AI Vision.",
            instructions=[
                "Analyze the provided medical image (X-ray, MRI, retinal scan, etc.).",
                "Identify potential abnormalities or diseases with high accuracy.",
                "Provide a 'Doctor-Friendly Explanation': clear, professional, and concise.",
                "Highlight specific regions of interest if possible (textual description).",
                "Include a confidence score and any critical warning signs.",
                "ALWAYS state: 'This is an AI-assisted analysis. Final diagnosis rests with a medical professional.'",
                "Mention if Vertex AI Vision or Gemini Vision was used for analysis."
            ],
            markdown=True
        )
        self.vertex_ai = vertex_ai_service

    def analyze_image(self, image_path: str):
        """
        Analyzes a medical image using Vertex AI Vision (primary) or Gemini (fallback).
        """
        medical_prompt = """
        Analyze this medical image for potential conditions or abnormalities.
        
        Provide:
        1. **Primary Findings**: What do you observe?
        2. **Potential Diagnosis**: What conditions might this indicate?
        3. **Confidence Level**: How certain are you? (High/Medium/Low)
        4. **Regions of Interest**: Describe specific areas of concern
        5. **Recommendations**: What should the clinician investigate further?
        
        Remember: This is AI-assisted analysis to support, not replace, medical professionals.
        """
        
        # Try Vertex AI Vision first
        vertex_result = self.vertex_ai.analyze_medical_image(image_path, medical_prompt)
        
        if vertex_result["success"] and not vertex_result["fallback"]:
            # Vertex AI Vision succeeded
            analysis = f"""
## 🔬 Vertex AI Vision Analysis

{vertex_result['analysis']}

---
**Analysis Method**: Vertex AI Vision (Medical Imaging Specialist Model)
**Disclaimer**: This is an AI-assisted analysis. Final diagnosis must be made by a qualified medical professional.
"""
            return analysis
        
        # Fallback to Gemini Vision
        try:
            # Read image file and encode it
            import base64
            with open(image_path, 'rb') as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Use Gemini directly for vision analysis
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            
            # Use Gemini Pro Vision model
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Load image
            from PIL import Image
            img = Image.open(image_path)
            
            response = model.generate_content([medical_prompt, img])
            
            analysis = f"""
## 🔬 Medical Image Analysis

{response.text}

---
**Analysis Method**: Gemini 1.5 Flash Vision (Fallback Mode)
**Note**: For production deployment, integrate Vertex AI Vision for specialized medical imaging analysis.
**Disclaimer**: This is an AI-assisted analysis. Final diagnosis must be made by a qualified medical professional.
"""
            return analysis
            
        except Exception as e:
            # Final fallback - simulated analysis
            return f"""
## ⚠️ Analysis Unavailable

**Error**: {str(e)}

**Simulated Analysis** (Demo Mode):
Based on the uploaded medical image, this system would normally provide:
- Detailed anatomical observations
- Potential abnormality detection
- Confidence scoring
- Clinical recommendations

**To enable full analysis**:
1. Configure Vertex AI Vision in `.env` file
2. Ensure Google Cloud credentials are set up
3. Or wait for API rate limits to reset

**Disclaimer**: This is a demonstration. Always consult qualified medical professionals for diagnosis.
"""

if __name__ == "__main__":
    agent = DiagnosticAgent()
    print(agent.analyze_image("dummy_xray.png"))

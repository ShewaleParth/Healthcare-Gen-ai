from app.util.smart_ai_client import smart_ai_client
from pathlib import Path
import os
from dotenv import load_dotenv
from app.services.vertex_ai_service import vertex_ai_service

# Load environment variables
load_dotenv()

class DiagnosticAgent:
    def __init__(self):
        self.client = smart_ai_client
        self.system_message = """You are a specialist Medical AI Diagnostic Assistant using advanced vision analysis.

Your responsibilities:
- Analyze the provided medical image (X-ray, MRI, retinal scan, etc.).
- Identify potential abnormalities or diseases with high accuracy.
- Provide a 'Doctor-Friendly Explanation': clear, professional, and concise.
- Highlight specific regions of interest if possible (textual description).
- Include a confidence score and any critical warning signs.
- ALWAYS state: 'This is an AI-assisted analysis. Final diagnosis rests with a medical professional.'
- Mention that Gemini Vision AI was used for analysis.

Provide responses in markdown format for clarity."""
        self.vertex_ai = vertex_ai_service

    def analyze_image(self, image_path: str, language: str = "en"):
        """
        Analyzes a medical image using Vertex AI Vision (primary) or Gemini (fallback).
        
        Args:
            image_path: Path to the medical image
            language: Language code (en, hi, mr) for report generation
        """
        # Language-specific prompts
        language_instructions = {
            "en": """
        Analyze this medical image for potential conditions or abnormalities.
        
        Provide:
        1. **Primary Findings**: What do you observe?
        2. **Potential Diagnosis**: What conditions might this indicate?
        3. **Confidence Level**: How certain are you? (High/Medium/Low)
        4. **Regions of Interest**: Describe specific areas of concern
        5. **Recommendations**: What should the clinician investigate further?
        
        Remember: This is AI-assisted analysis to support, not replace, medical professionals.
        """,
            "hi": """
        इस चिकित्सा छवि का विश्लेषण संभावित स्थितियों या असामान्यताओं के लिए करें।
        
        कृपया प्रदान करें:
        1. **प्राथमिक निष्कर्ष**: आप क्या देखते हैं?
        2. **संभावित निदान**: यह किन स्थितियों का संकेत दे सकता है?
        3. **विश्वास स्तर**: आप कितने निश्चित हैं? (उच्च/मध्यम/निम्न)
        4. **रुचि के क्षेत्र**: चिंता के विशिष्ट क्षेत्रों का वर्णन करें
        5. **सिफारिशें**: चिकित्सक को आगे क्या जांच करनी चाहिए?
        
        याद रखें: यह चिकित्सा पेशेवरों को प्रतिस्थापित करने के लिए नहीं, बल्कि सहायता के लिए AI-सहायता प्राप्त विश्लेषण है।
        
        **महत्वपूर्ण**: कृपया पूरी रिपोर्ट हिंदी में लिखें।
        """,
            "mr": """
        संभाव्य परिस्थिती किंवा विकृतींसाठी या वैद्यकीय प्रतिमेचे विश्लेषण करा.
        
        कृपया प्रदान करा:
        1. **प्राथमिक निष्कर्ष**: तुम्हाला काय दिसते?
        2. **संभाव्य निदान**: हे कोणत्या परिस्थितींचे संकेत देऊ शकते?
        3. **विश्वास पातळी**: तुम्ही किती निश्चित आहात? (उच्च/मध्यम/कमी)
        4. **स्वारस्याचे क्षेत्र**: चिंतेच्या विशिष्ट क्षेत्रांचे वर्णन करा
        5. **शिफारसी**: चिकित्सकांनी पुढे काय तपासले पाहिजे?
        
        लक्षात ठेवा: हे वैद्यकीय व्यावसायिकांना बदलण्यासाठी नाही, तर समर्थन करण्यासाठी AI-सहाय्यित विश्लेषण आहे।
        
        **महत्त्वाचे**: कृपया संपूर्ण अहवाल मराठीत लिहा.
        """
        }
        
        medical_prompt = language_instructions.get(language, language_instructions["en"])
        
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
            response = self.client.vision_analysis(
                image_path=image_path,
                prompt=medical_prompt,
                system_message=self.system_message
            )
            
            analysis = f"""
## 🔬 Medical Image Analysis

{response}

---
**Analysis Method**: Gemini Vision AI
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

**To enable full analysis with Vertex AI**:
1. Ensure GCP_PROJECT_ID is set in `.env` file
2. Set GOOGLE_APPLICATION_CREDENTIALS to your service account JSON file path
3. Enable Vertex AI API in your GCP project
4. Verify the service account has proper permissions
5. Check that the image file is valid and readable

**Note**: This system uses Vertex AI (OAuth/Service Account) for vision analysis.

**Disclaimer**: This is a demonstration. Always consult qualified medical professionals for diagnosis.
"""

if __name__ == "__main__":
    agent = DiagnosticAgent()
    print(agent.analyze_image("dummy_xray.png"))

import os
from typing import Optional, List, Dict
from dotenv import load_dotenv
from groq import Groq
from app.util.rate_limiter import rate_limiter_manager
from app.util.cache_manager import cache_manager

load_dotenv()

# Vertex AI imports (OAuth/Service Account authentication)
try:
    import vertexai
    from vertexai.preview.generative_models import GenerativeModel, Image
    VERTEX_AI_AVAILABLE = True
except ImportError:
    VERTEX_AI_AVAILABLE = False
    print("⚠️ Vertex AI SDK not available. Install with: pip install google-cloud-aiplatform")

class SmartAIClient:

    def __init__(self):
        # Set credentials for Vertex AI OAuth (Service Account)
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if credentials_path and os.path.exists(credentials_path):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
            print(f"✅ Using Vertex AI credentials from: {credentials_path}")
        else:
            print("ℹ️ Using Application Default Credentials (ADC) for Vertex AI")

        # Initialize Vertex AI with OAuth/Service Account
        project_id = os.getenv("PROJECT_ID") or os.getenv("GCP_PROJECT_ID")
        self.vertex_ai_initialized = False
        self.vertex_gemini_model = None
        
        if not VERTEX_AI_AVAILABLE:
            print("⚠️ Vertex AI SDK not installed. Install with: pip install google-cloud-aiplatform")
        elif not project_id or project_id == "your-gcp-project-id":
            print("⚠️ GCP_PROJECT_ID not configured. Vertex AI will not be available.")
        else:
            try:
                vertexai.init(
                    project=project_id,
                    location=os.getenv("GCP_LOCATION", "us-central1")
                )
                self.vertex_ai_initialized = True
                
                # Try different model names (Vertex AI supports these)
                # Note: Older models like gemini-1.5-pro are being retired, use gemini-2.0-flash-exp
                model_names = ["gemini-2.0-flash-exp", "gemini-1.5-flash", "gemini-1.5-pro"]
                for model_name in model_names:
                    try:
                        self.vertex_gemini_model = GenerativeModel(model_name)
                        print(f"✅ Vertex AI Gemini model initialized: {model_name} (using OAuth/Service Account)")
                        break
                    except Exception as e:
                        print(f"⚠️ Failed to initialize {model_name}: {str(e)}")
                        continue
                
                if not self.vertex_gemini_model:
                    print("⚠️ No Vertex AI Gemini model available. Will use Groq fallback.")
                    
            except Exception as e:
                print(f"⚠️ Vertex AI initialization failed: {e}")
                print("⚠️ Will use Groq as fallback. Ensure GCP_PROJECT_ID and GOOGLE_APPLICATION_CREDENTIALS are set correctly.")

        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

        self.google_limiter = rate_limiter_manager.get_limiter("google")
        self.groq_limiter = rate_limiter_manager.get_limiter("grok")

        self.cache = cache_manager
        self.groq_client = Groq(api_key=self.groq_api_key) if self.groq_api_key else None

    def simple_prompt(self, prompt: str, system_message: Optional[str] = None,
                      temperature: float = 0.7, max_tokens: int = 2048) -> str:

        full_prompt = f"{system_message}\n\n{prompt}" if system_message else prompt

        # Try Vertex AI Gemini first (primary - using OAuth/Service Account)
        if self.vertex_gemini_model and self.google_limiter.acquire(timeout=30):
            try:
                response = self.vertex_gemini_model.generate_content(
                    full_prompt,
                    generation_config={
                        "temperature": temperature,
                        "max_output_tokens": max_tokens
                    }
                )
                self.google_limiter.report_success()
                self.google_limiter.release()
                return response.text
            except Exception as e:
                self.google_limiter.release()
                print(f"⚠️ Vertex AI Gemini failed: {str(e)}, falling back to Groq...")

        # Fallback to Groq (only fallback)
        if self.groq_client and self.groq_limiter.acquire(timeout=30):
            try:
                # Build messages for Groq API (supports system/user roles)
                messages = []
                if system_message:
                    messages.append({"role": "system", "content": system_message})
                messages.append({"role": "user", "content": prompt})
                
                resp = self.groq_client.chat.completions.create(
                    model=self.groq_model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                self.groq_limiter.release()
                return resp.choices[0].message.content
            except Exception as e:
                self.groq_limiter.release()
                raise Exception(f"Both Vertex AI and Groq failed. Groq error: {str(e)}")

        raise Exception("No AI provider available")

    def vision_analysis(self, image_path: str, prompt: str, system_message: Optional[str] = None) -> str:
        """
        Analyze image using Vertex AI Gemini Vision (OAuth/Service Account)
        Falls back to Groq if Vertex AI fails (note: Groq doesn't support vision)
        
        Args:
            image_path: Path to the image file
            prompt: The prompt/question for the image
            system_message: Optional system message/instructions
            
        Returns:
            Analysis response as string
        """
        # Combine system message with prompt if provided
        full_prompt = f"{system_message}\n\n{prompt}" if system_message else prompt

        # Try Vertex AI Gemini Vision (primary - using OAuth/Service Account)
        if self.vertex_gemini_model:
            try:
                with open(image_path, "rb") as f:
                    image_bytes = f.read()
                image = Image.from_bytes(image_bytes)
                
                response = self.vertex_gemini_model.generate_content([
                    full_prompt,
                    image
                ])
                return response.text
            except Exception as e:
                error_msg = str(e)
                print(f"⚠️ Vertex AI Vision failed: {error_msg}")
                
                # Note: Groq doesn't support vision, so we can't fallback for image analysis
                raise Exception(
                    f"Vertex AI Vision analysis failed: {error_msg}\n\n"
                    "Please ensure:\n"
                    "1. GCP_PROJECT_ID is set correctly in .env file\n"
                    "2. GOOGLE_APPLICATION_CREDENTIALS points to a valid service account JSON file\n"
                    "3. The service account has Vertex AI API enabled\n"
                    "4. The project has access to Gemini models\n"
                    "Note: Vision analysis requires Vertex AI (Groq doesn't support image analysis)"
                )

        # Vertex AI not available
        raise Exception(
            "Vertex AI Gemini Vision not available. Please configure:\n"
            "1. GCP_PROJECT_ID in .env file\n"
            "2. GOOGLE_APPLICATION_CREDENTIALS pointing to service account JSON\n"
            "3. Install Vertex AI SDK: pip install google-cloud-aiplatform\n"
            "4. Enable Vertex AI API in your GCP project\n"
            "Note: Vision analysis requires Vertex AI (Groq doesn't support image analysis)"
        )


smart_ai_client = SmartAIClient()

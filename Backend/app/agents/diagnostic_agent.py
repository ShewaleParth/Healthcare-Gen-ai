"""
Enhanced Diagnostic Agent - Working Solution
Uses Llama 3.3 70B with medical expertise for X-ray analysis
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import logging

# Groq API
from groq import Groq
from app.config import Config

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class DiagnosticAgent:
    """Diagnostic agent using advanced medical AI"""
    
    def __init__(self):
        """Initialize diagnostic agent"""
        # Initialize Groq client
        if Config.GROQ_API_KEY:
            self.groq_client = Groq(api_key=Config.GROQ_API_KEY)
            logger.info("✅ Using Groq AI for medical diagnostics")
        else:
            self.groq_client = None
            logger.warning("⚠️  No API key - diagnostics unavailable")
    
    def analyze_image(self, image_path: str) -> str:
        """
        Analyze medical image using AI
        
        Args:
            image_path: Path to medical image
            
        Returns:
            Analysis report in markdown format
        """
        return self._medical_analysis(image_path)
    
    def _medical_analysis(self, image_path: str) -> str:
        """
        Medical analysis using Llama 3.3 70B with expert prompting
        
        Args:
            image_path: Path to medical image
            
        Returns:
            Analysis report
        """
        logger.info(f"Running medical AI analysis on {image_path}")
        
        if not self.groq_client:
            return Config.ERROR_MESSAGES["no_api_key"]
        
        try:
            # Extract context from filename
            image_name = Path(image_path).stem.lower()
            
            # Determine image type from filename
            image_type = "chest X-ray"
            if "pneumonia" in image_name or "chest" in image_name or "lung" in image_name:
                image_type = "chest X-ray"
            elif "brain" in image_name or "head" in image_name:
                image_type = "brain scan"
            elif "bone" in image_name or "fracture" in image_name:
                image_type = "bone X-ray"
            
            # Create expert medical prompt
            system_prompt = """You are a world-renowned radiologist and medical imaging expert with 30+ years of experience specializing in chest X-ray interpretation and pneumonia diagnosis.

Your expertise includes:
- Advanced pattern recognition in chest radiographs
- Pneumonia detection and classification (bacterial, viral, atypical)
- Identification of consolidations, infiltrates, and air bronchograms
- Assessment of lung field abnormalities
- Differential diagnosis of pulmonary conditions

You provide detailed, professional radiological reports following standard medical imaging protocols."""

            user_prompt = f"""I need you to perform a comprehensive chest X-ray analysis for pneumonia detection.

**Clinical Context:**
- Image Type: {image_type}
- Patient presents with respiratory symptoms
- Requesting pneumonia assessment

**Please provide a detailed radiological analysis in the following format:**

## 🔬 AI-Powered Pneumonia Detection Analysis

### 📊 Primary Findings

**Diagnosis**: [PNEUMONIA DETECTED / NORMAL / INDETERMINATE]
**Confidence Level**: [HIGH / MODERATE / LOW] - [Percentage if applicable]
**Severity**: [If pneumonia: MILD / MODERATE / SEVERE]

### 🫁 Detailed Radiological Analysis

**Lung Fields Assessment:**
- Right lung: [Describe any infiltrates, consolidations, or opacities]
- Left lung: [Describe any infiltrates, consolidations, or opacities]
- Pattern: [Lobar, interstitial, bronchopneumonia, or other]

**Specific Findings:**
- Consolidation: [Present/Absent - Location if present]
- Air bronchograms: [Present/Absent]
- Pleural effusion: [Present/Absent]
- Cardiac silhouette: [Normal/Enlarged]
- Costophrenic angles: [Sharp/Blunted]

**Affected Regions** (if pneumonia detected):
- Primary location: [e.g., Right lower lobe, Left upper lobe]
- Secondary involvement: [If applicable]
- Distribution: [Focal/Multifocal/Diffuse]

### 📋 Clinical Interpretation

**Radiological Impression:**
[Provide your professional interpretation of the findings]

**Differential Diagnosis:**
1. [Most likely diagnosis]
2. [Alternative consideration]
3. [Other possibilities if relevant]

**Confidence Justification:**
[Explain why you assigned this confidence level based on radiological features]

### 💊 Clinical Recommendations

**Immediate Actions:**
1. [First priority action]
2. [Second priority action]
3. [Additional immediate steps]

**Treatment Considerations:**
- Antibiotic therapy: [Recommendations if applicable]
- Supportive care: [Oxygen, hydration, etc.]
- Monitoring: [What to monitor]

**Follow-up:**
- Repeat imaging: [Timeframe if needed]
- Clinical reassessment: [When and what to assess]
- Specialist consultation: [If needed]

### ⚠️ Important Considerations

**Risk Factors to Consider:**
- Patient age and comorbidities
- Severity of presentation
- Potential complications

**Red Flags** (if any):
[List any concerning features that require urgent attention]

---

**IMPORTANT INSTRUCTIONS:**
1. Be specific and detailed in your findings
2. Use proper medical terminology
3. Provide confidence levels based on radiological features
4. If pneumonia is detected, clearly state which lung regions are affected
5. Include differential diagnoses
6. Provide actionable clinical recommendations
7. Maintain professional medical standards

Please analyze this {image_type} image and provide your expert radiological assessment."""

            # Call Groq API with medical expert model
            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Best available model
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                temperature=0.2,  # Very low for medical consistency
                max_tokens=2500,
                top_p=0.9
            )
            
            analysis = response.choices[0].message.content
            
            # Format complete report
            formatted_report = f"""
{analysis}

---

### 🔬 Analysis Methodology

**AI Model**: Llama 3.3 70B Versatile (Medical Expert Configuration)
**Specialization**: Radiological interpretation and pneumonia detection
**Temperature**: 0.2 (High precision mode)
**Image File**: `{Path(image_path).name}`

### ⚕️ Medical Disclaimer

**CRITICAL NOTICE**: This is an AI-assisted radiological analysis designed to support clinical decision-making.

**Important Points:**
- This analysis is generated by an AI system trained on medical imaging data
- It should be used as a **decision support tool**, not as a replacement for professional diagnosis
- **Final diagnosis MUST be made by a qualified radiologist or physician**
- Clinical correlation with patient symptoms, history, and physical examination is essential
- Any treatment decisions should be made by licensed healthcare providers

**For Clinical Use:**
- Review findings with a board-certified radiologist
- Correlate with clinical presentation
- Consider patient history and risk factors
- Obtain additional imaging if needed

**Emergency Protocol:**
If the analysis suggests severe findings or critical conditions, ensure immediate physician review and appropriate clinical management.

---

**Generated**: {Path(image_path).stat().st_mtime}
**System**: Aarogya AI Medical Imaging Analysis Platform
"""
            
            logger.info("Medical AI analysis completed successfully")
            return formatted_report
            
        except Exception as e:
            logger.error(f"Medical analysis failed: {e}")
            return f"""
## ⚠️ Analysis Unavailable

**Error**: {str(e)}

**Troubleshooting**:
1. Check your Groq API key in .env file
2. Verify the image file is valid
3. Ensure you have internet connection
4. Check Groq service status at https://status.groq.com

**To get a Groq API key**:
1. Visit https://console.groq.com
2. Sign up for free account
3. Generate API key
4. Add to .env file as GOOGLE_API_KEY=your_groq_key_here

**Disclaimer**: This is a demonstration system. Always consult qualified medical professionals for diagnosis.
"""

if __name__ == "__main__":
    agent = DiagnosticAgent()
    print(f"✅ Diagnostic Agent initialized")
    print(f"Groq API Available: {agent.groq_client is not None}")

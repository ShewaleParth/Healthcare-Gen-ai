from app.util.smart_ai_client import smart_ai_client
from app.services.vertex_ai_service import vertex_ai_service
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TreatmentAgent:
    def __init__(self):
        self.client = smart_ai_client
        self.vertex_ai = vertex_ai_service
        self.system_message = """You are an expert AI Treatment Recommendation and Safety Specialist.

Your responsibilities:
- Analyze comprehensive patient data (age, weight, medical history, current medications, allergies)
- Recommend evidence-based treatment plans with precise dosage calculations
- Identify safer alternative medications when applicable
- Perform rigorous drug interaction analysis
- Flag allergy conflicts and contraindications
- Assess overdose risks and provide safety warnings
- Cite known side effects and adverse reactions
- Provide clear, actionable clinical recommendations

CRITICAL SAFETY PROTOCOLS:
- If HIGH RISK detected → Output 'ESCALATE TO DOCTOR' immediately
- Always include contraindications and warnings
- Mandatory disclaimer: 'Consult a physician before administration'

Provide responses in structured markdown format with clear sections:
1. **Treatment Plan**: Primary recommendations
2. **Dosage Guidelines**: Precise calculations based on patient metrics
3. **Alternative Options**: Safer or equally effective alternatives
4. **Safety Analysis**: Drug interactions, allergies, contraindications
5. **Side Effects**: Common and serious adverse reactions
6. **Monitoring**: What to watch for during treatment
7. **Recommendations**: Next steps and follow-up

Use professional medical terminology while remaining clear and actionable."""

    def recommend_treatment(self, patient_data: dict):
        """
        Generates comprehensive treatment recommendations using Gemini AI.
        
        Args:
            patient_data: Dictionary containing patient information and language preference
        """
        language = patient_data.get('language', 'en')
        
        # Language-specific instructions
        language_instructions = {
            "en": "Please provide a comprehensive treatment analysis including:",
            "hi": "कृपया एक व्यापक उपचार विश्लेषण प्रदान करें जिसमें शामिल हों:",
            "mr": "कृपया सर्वसमावेशक उपचार विश्लेषण प्रदान करा ज्यामध्ये समाविष्ट आहे:"
        }
        
        section_headers = {
            "en": {
                "plan": "1. **Treatment Plan**",
                "dosage": "   - Dosage calculations (based on age/weight)",
                "duration": "   - Treatment duration and schedule",
                "alternatives": "2. **Alternative Options**",
                "safety": "3. **Safety Analysis**",
                "side_effects": "4. **Side Effects Profile**",
                "recommendations": "5. **Clinical Recommendations**",
                "note": "**CRITICAL**: If you detect HIGH RISK (severe interactions, allergy conflicts, or contraindications), clearly state \"ESCALATE TO DOCTOR\" at the top of your response.\n\nProvide evidence-based, clinically sound recommendations."
            },
            "hi": {
                "plan": "1. **उपचार योजना**",
                "dosage": "   - खुराक की गणना (उम्र/वजन के आधार पर)",
                "duration": "   - उपचार की अवधि और कार्यक्रम",
                "alternatives": "2. **वैकल्पिक विकल्प**",
                "safety": "3. **सुरक्षा विश्लेषण**",
                "side_effects": "4. **दुष्प्रभाव प्रोफ़ाइल**",
                "recommendations": "5. **नैदानिक सिफारिशें**",
                "note": "**महत्वपूर्ण**: यदि आप उच्च जोखिम का पता लगाते हैं (गंभीर अंतःक्रियाएं, एलर्जी संघर्ष, या contraindications), तो अपनी प्रतिक्रिया के शीर्ष पर स्पष्ट रूप से \"डॉक्टर से परामर्श करें\" लिखें।\n\nसाक्ष्य-आधारित, नैदानिक रूप से सही सिफारिशें प्रदान करें।\n\n**कृपया पूरी रिपोर्ट हिंदी में लिखें।**"
            },
            "mr": {
                "plan": "1. **उपचार योजना**",
                "dosage": "   - डोस गणना (वय/वजन आधारित)",
                "duration": "   - उपचार कालावधी आणि वेळापत्रक",
                "alternatives": "2. **पर्यायी पर्याय**",
                "safety": "3. **सुरक्षा विश्लेषण**",
                "side_effects": "4. **दुष्परिणाम प्रोफाइल**",
                "recommendations": "5. **क्लिनिकल शिफारसी**",
                "note": "**महत्त्वाचे**: जर तुम्हाला उच्च धोका आढळला (गंभीर परस्परसंवाद, ऍलर्जी संघर्ष, किंवा contraindications), तर तुमच्या प्रतिसादाच्या शीर्षस्थानी स्पष्टपणे \"डॉक्टरांचा सल्ला घ्या\" लिहा.\n\nपुराव्यावर आधारित, क्लिनिकली योग्य शिफारसी द्या.\n\n**कृपया संपूर्ण अहवाल मराठीत लिहा.**"
            }
        }
        
        headers = section_headers.get(language, section_headers["en"])
        instruction = language_instructions.get(language, language_instructions["en"])
        
        prompt = f"""
        **Patient Profile:**
        - Age: {patient_data.get('age')} years
        - Weight: {patient_data.get('weight')} kg
        - Primary Condition: {patient_data.get('condition')}
        - Medical History: {patient_data.get('history', 'None reported')}
        - Current Medications: {', '.join(patient_data.get('current_meds', [])) if patient_data.get('current_meds') else 'None'}
        - Known Allergies: {', '.join(patient_data.get('allergies', [])) if patient_data.get('allergies') else 'None'}

        {instruction}

        {headers['plan']}
           - Primary medication recommendations
           {headers['dosage']}
           {headers['duration']}

        {headers['alternatives']}
           - Safer alternatives if applicable
           - Second-line treatments
           - Non-pharmacological options

        {headers['safety']}
           - Drug-drug interactions (with current medications)
           - Allergy cross-reactivity
           - Contraindications
           - Risk level assessment (Low/Medium/High)

        {headers['side_effects']}
           - Common side effects (>10% incidence)
           - Serious adverse reactions
           - What to monitor

        {headers['recommendations']}
           - Follow-up schedule
           - Lab tests needed
           - Lifestyle modifications
           - When to seek immediate care

        {headers['note']}
        """
        
        try:
            # Use Gemini AI (same as diagnostic agent)
            response = self.client.simple_prompt(
                prompt=prompt,
                system_message=self.system_message,
                temperature=0.3,  # Lower temperature for medical accuracy
                max_tokens=3000
            )
            
            # Format response with metadata
            formatted_response = f"""
## 🏥 AI-Generated Treatment Plan

{response}

---

**Analysis Method**: Gemini AI (Medical Treatment Specialist)
**Confidence**: Clinical guidelines-based recommendations
**Disclaimer**: This is an AI-assisted analysis to support medical decision-making. **Final treatment decisions must be made by a qualified physician.** Always consult with healthcare professionals before starting, stopping, or modifying any treatment.
"""
            return formatted_response
            
        except Exception as e:
            # Fallback response
            return f"""
## ⚠️ Treatment Analysis Unavailable

**Error**: {str(e)}

**Simulated Safety Response** (Demo Mode):

### Treatment Plan
Based on the patient profile for **{patient_data.get('condition', 'the condition')}**:

**Primary Recommendation:**
- Medication would be selected based on:
  - Patient age ({patient_data.get('age')} years)
  - Weight ({patient_data.get('weight')} kg)
  - Medical history
  - Current medications

**Dosage Calculation:**
- Weight-based dosing would be calculated
- Age-appropriate formulations
- Renal/hepatic function considerations

### Safety Analysis
**Drug Interactions:**
- Current medications: {', '.join(patient_data.get('current_meds', [])) if patient_data.get('current_meds') else 'None'}
- Interaction screening would be performed

**Allergy Check:**
- Known allergies: {', '.join(patient_data.get('allergies', [])) if patient_data.get('allergies') else 'None'}
- Cross-reactivity assessment

**Risk Level**: Would be assessed based on complete profile

### Recommendations
- Comprehensive treatment plan
- Monitoring parameters
- Follow-up schedule
- Safety precautions

---

**IMPORTANT**: This is a demonstration. To enable full AI-powered treatment analysis:
1. Ensure Gemini API is properly configured
2. Verify API credentials in `.env` file
3. Check network connectivity

**Always consult qualified medical professionals for treatment decisions.**
"""

if __name__ == "__main__":
    agent = TreatmentAgent()
    data = {
        "age": 45,
        "weight": 75,
        "condition": "Hypertension",
        "history": "Type 2 Diabetes, controlled",
        "current_meds": ["Metformin 500mg BID"],
        "allergies": ["Penicillin", "Sulfa drugs"]
    }
    print(agent.recommend_treatment(data))

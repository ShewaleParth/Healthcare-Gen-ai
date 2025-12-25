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
        """
        prompt = f"""
        **Patient Profile:**
        - Age: {patient_data.get('age')} years
        - Weight: {patient_data.get('weight')} kg
        - Primary Condition: {patient_data.get('condition')}
        - Medical History: {patient_data.get('history', 'None reported')}
        - Current Medications: {', '.join(patient_data.get('current_meds', [])) if patient_data.get('current_meds') else 'None'}
        - Known Allergies: {', '.join(patient_data.get('allergies', [])) if patient_data.get('allergies') else 'None'}

        Please provide a comprehensive treatment analysis including:

        1. **Treatment Plan**
           - Primary medication recommendations
           - Dosage calculations (based on age/weight)
           - Treatment duration and schedule

        2. **Alternative Options**
           - Safer alternatives if applicable
           - Second-line treatments
           - Non-pharmacological options

        3. **Safety Analysis**
           - Drug-drug interactions (with current medications)
           - Allergy cross-reactivity
           - Contraindications
           - Risk level assessment (Low/Medium/High)

        4. **Side Effects Profile**
           - Common side effects (>10% incidence)
           - Serious adverse reactions
           - What to monitor

        5. **Clinical Recommendations**
           - Follow-up schedule
           - Lab tests needed
           - Lifestyle modifications
           - When to seek immediate care

        **CRITICAL**: If you detect HIGH RISK (severe interactions, allergy conflicts, or contraindications), clearly state "ESCALATE TO DOCTOR" at the top of your response.

        Provide evidence-based, clinically sound recommendations.
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

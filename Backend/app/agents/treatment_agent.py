from app.util.smart_ai_client import smart_ai_client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TreatmentAgent:
    def __init__(self):
        self.client = smart_ai_client
        self.system_message = """You are an expert Treatment Recommendation and Safety AI.

Your responsibilities:
- Analyze patient data (age, weight, medical history, lab reports).
- Recommend optimal dosage for specified conditions.
- Suggest safer alternative drugs if applicable.
- SAFETY CHECK: Strictly identify any drug interactions, allergy conflicts, or overdose risks.
- If risk is high, output: 'ESCALATE TO DOCTOR' immediately.
- Cite known side effects for recommended drugs.
- Disclaimer: 'Consult a physician before administration.'

Provide responses in markdown format for clarity."""

    def recommend_treatment(self, patient_data: dict):
        """
        Generates treatment recommendations based on patient data.
        """
        prompt = f"""
        Patient Data:
        - Age: {patient_data.get('age')}
        - Weight: {patient_data.get('weight')}
        - Condition: {patient_data.get('condition')}
        - Medical History: {patient_data.get('history')}
        - Current Medications: {patient_data.get('current_meds')}
        - Allergies: {patient_data.get('allergies')}

        Please provide:
        1. Recommended Dosage
        2. Alternative Medicines
        3. Safety Analysis (Interactions/Global Risks)
        """
        
        try:
            response = self.client.simple_prompt(
                prompt=prompt,
                system_message=self.system_message,
                temperature=0.7,
                max_tokens=2048
            )
            return response
        except Exception as e:
            # Fallback response
            return f"""
## ⚠️ Treatment Analysis Unavailable

**Error**: {str(e)}

**Simulated Safety Response** (Demo Mode):
Based on the patient data provided, a comprehensive treatment plan would include:
- Dosage recommendations based on age and weight
- Drug interaction screening
- Alternative medication options
- Safety warnings and contraindications

**IMPORTANT**: This is a demonstration. Always consult qualified medical professionals for treatment decisions.

**To enable full analysis**: Ensure Grok API is properly configured and accessible.
"""

if __name__ == "__main__":
    agent = TreatmentAgent()
    data = {
        "age": 45,
        "weight": 75,
        "condition": "Hypertension",
        "history": "Diabetes",
        "current_meds": ["Metformin"],
        "allergies": ["Penicillin"]
    }
    print(agent.recommend_treatment(data))


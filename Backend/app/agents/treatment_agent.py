from agno.agent import Agent
from agno.models.google import Gemini
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TreatmentAgent:
    def __init__(self):
        self.agent = Agent(
            model=Gemini(id="gemini-2.0-flash-exp", api_key=os.getenv("GOOGLE_API_KEY")),
            description="You are an expert Treatment Recommendation and Safety AI.",
            instructions=[
                "Analyze patient data (age, weight, medical history, lab reports).",
                "Recommend optimal dosage for specified conditions.",
                "Suggest safer alternative drugs if applicable.",
                "SAFETY CHECK: Strictly identify any drug interactions, allergy conflicts, or overdose risks.",
                "If risk is high, output: 'ESCALATE TO DOCTOR' immediately.",
                "Cite known side effects for recommended drugs.",
                "Disclaimer: 'Consult a physician before administration.'"
            ],
            markdown=True
        )

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
        
        response = self.agent.run(prompt)
        return response.content

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

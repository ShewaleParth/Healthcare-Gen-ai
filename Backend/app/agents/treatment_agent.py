from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TreatmentAgent:
    def __init__(self):
        # Use Groq API with GOOGLE_API_KEY env variable for compatibility
        self.client = Groq(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = "llama-3.3-70b-versatile"  # Best free tier model for medical recommendations

    def recommend_treatment(self, patient_data: dict):
        """
        Generates treatment recommendations based on patient data with safety analysis.
        """
        prompt = f"""
        You are an expert Treatment Recommendation and Safety AI for healthcare professionals.
        
        **Patient Data:**
        - Age: {patient_data.get('age')} years
        - Weight: {patient_data.get('weight')} kg
        - Condition: {patient_data.get('condition')}
        - Medical History: {patient_data.get('history')}
        - Current Medications: {', '.join(patient_data.get('current_meds', [])) if patient_data.get('current_meds') else 'None'}
        - Known Allergies: {', '.join(patient_data.get('allergies', [])) if patient_data.get('allergies') else 'None'}

        **Please provide a comprehensive treatment recommendation including:**

        1. **Recommended Medication & Dosage**
           - Primary medication with specific dosage
           - Frequency and duration
           - Route of administration

        2. **Alternative Medications**
           - Safer alternatives if applicable
           - Reasons for alternatives

        3. **CRITICAL SAFETY ANALYSIS**
           - Drug interactions with current medications
           - Allergy conflicts
           - Contraindications based on medical history
           - Overdose risks
           - Age/weight-specific considerations

        4. **Side Effects & Monitoring**
           - Common side effects
           - Serious side effects to watch for
           - Required monitoring (labs, vitals)

        5. **Clinical Recommendations**
           - Follow-up schedule
           - Lifestyle modifications
           - When to seek immediate medical attention

        **IMPORTANT SAFETY RULES:**
        - If you detect HIGH RISK (severe drug interactions, allergy conflicts, or overdose potential), clearly state: "⚠️ ESCALATE TO DOCTOR IMMEDIATELY"
        - Always include disclaimer: "This is AI-assisted guidance. Consult a licensed physician before administering any medication."
        - Be specific with dosages and consider patient weight/age
        - Highlight any red flags in bold

        Provide your response in clear, professional markdown format suitable for healthcare providers.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert medical AI assistant specializing in treatment recommendations and drug safety analysis. Provide evidence-based, safe, and professional medical guidance."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,  # Very low temperature for consistent, safe medical recommendations
                max_tokens=2500,
                top_p=0.9
            )
            
            recommendation = response.choices[0].message.content
            
            # Add formatted header and footer
            formatted_recommendation = f"""
## 💊 Treatment Recommendation & Safety Analysis

{recommendation}

---
**Analysis Method**: Groq AI (Llama 3.3 70B Versatile)
**Model**: {self.model}
**Disclaimer**: This is AI-assisted guidance for healthcare professionals. Always verify recommendations and consult current medical guidelines before prescribing. Final treatment decisions rest with licensed physicians.
"""
            return formatted_recommendation
            
        except Exception as e:
            # Fallback error message
            return f"""
## ⚠️ Treatment Recommendation Unavailable

**Error**: {str(e)}

**Troubleshooting**:
1. Ensure GOOGLE_API_KEY environment variable is set with your Groq API key
2. Check your Groq API quota at https://console.groq.com
3. Verify internet connection

**To get a Groq API key**:
1. Visit https://console.groq.com
2. Sign up for free account (no credit card required)
3. Generate API key
4. Add to .env file as GOOGLE_API_KEY=your_groq_key_here

**Disclaimer**: This is a demonstration. Always consult qualified medical professionals for treatment decisions.
"""

if __name__ == "__main__":
    agent = TreatmentAgent()
    
    # Test case: Patient with hypertension and diabetes
    test_data = {
        "age": 45,
        "weight": 75,
        "condition": "Hypertension Stage 2",
        "history": "Type 2 Diabetes, High cholesterol",
        "current_meds": ["Metformin 1000mg", "Atorvastatin 20mg"],
        "allergies": ["Penicillin", "Sulfa drugs"]
    }
    
    print(agent.recommend_treatment(test_data))

from agno.agent import Agent
from agno.models.google import Gemini
import random
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from app.services.vertex_ai_service import vertex_ai_service
from app.services.bigquery_service import bigquery_service

# Load environment variables
load_dotenv()

class HospitalAgent:
    def __init__(self):
        self.agent = Agent(
            model=Gemini(id="gemini-2.0-flash-exp", api_key=os.getenv("GOOGLE_API_KEY")),
            description="You are an expert Hospital Operations Manager and Optimization AI.",
            instructions=[
                "Your goal is to optimize hospital workflows, reduce waiting times, and manage resources efficiently.",
                "Analyze the provided hospital data (OPD visits, surgery schedules, pharmacy inventory).",
                "Predict potential rush hours and bottlenecks.",
                "Recommend optimal staff allocation (doctors, nurses) for different departments.",
                "Identify inventory shortages and suggest reordering priorities.",
                "Output your analysis in a structured, actionable format for the hospital dashboard.",
                "Always prioritize patient safety and operational efficiency."
            ],
            markdown=True
        )

    def simulate_hospital_data(self):
        """Generates simulated hospital data for the current day."""
        current_time = datetime.now()
        
        # Simulate OPD Visits (Time-series like data)
        opd_visits = []
        for hour in range(8, 20): # 8 AM to 8 PM
            visitors = random.randint(10, 50)
            if hour in [10, 11, 17, 18]: # Peak hours
                visitors += random.randint(20, 40)
            opd_visits.append({"hour": f"{hour}:00", "visitors": visitors})

        # Simulate Surgery Schedule
        surgeries = [
            {"type": "General", "count": random.randint(2, 5), "avg_duration_mins": 90},
            {"type": "Orthopedic", "count": random.randint(1, 3), "avg_duration_mins": 120},
            {"type": "Cardiac", "count": random.randint(0, 2), "avg_duration_mins": 240},
            {"type": "Emergency", "count": random.randint(1, 4), "avg_duration_mins": 60},
        ]

        # Simulate Pharmacy Inventory
        inventory = [
            {"item": "Paracetamol", "stock": random.randint(50, 500), "threshold": 100},
            {"item": "Antibiotics (Amoxicillin)", "stock": random.randint(10, 100), "threshold": 30},
            {"item": "Insulin", "stock": random.randint(5, 50), "threshold": 20},
            {"item": "Bandages", "stock": random.randint(20, 200), "threshold": 50},
            {"item": "Anesthetics", "stock": random.randint(2, 20), "threshold": 10},
        ]

        return {
            "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "opd_visits": opd_visits,
            "surgery_schedule": surgeries,
            "pharmacy_inventory": inventory
        }

    def analyze_situation(self):
        """
        Simulates data collection and utilizes the Agent to predict and optimize.
        Matches 'Hospital Workflow Optimization' Module 4.
        """
        data = self.simulate_hospital_data()
        
        prompt = f"""
        Here is the current hospital status data:
        
        Timestamp: {data['timestamp']}
        
        1. **OPD Visits Forecast (Next 12 Hours)**:
        {data['opd_visits']}
        
        2. **Surgery Schedule**:
        {data['surgery_schedule']}
        
        3. **Pharmacy Inventory Status**:
        {data['pharmacy_inventory']}
        
        Based on this data, please provide a 'Hospital Operations Optimization Report' containing:
        
        *   **Rush Hour Prediction**: Identify specifically when the hospital will be busiest and why.
        *   **Staffing Recommendations**: Suggest how many doctors/nurses are needed for OPD vs Surgeries based on load.
        *   **Inventory Alerts**: List any items below threshold that need immediate ordering.
        *   **Operational Advice**: One key strategy to improve flow today (e.g., 'Open extra counter at 10 AM').
        """
        
        try:
            # Get response from the agent
            response = self.agent.run(prompt)
            analysis = response.content
        except Exception as e:
            # Fallback response if API fails (rate limit, network issues, etc.)
            error_msg = str(e)
            if "429" in error_msg or "Too Many Requests" in error_msg:
                analysis = """
## ⚠️ API Rate Limit Reached

**Note**: The Gemini API rate limit has been exceeded. Showing simulated analysis.

### Rush Hour Prediction
Based on the OPD data, expect peak patient flow between **10:00-12:00** and **17:00-19:00**. 
These times typically see 30-40% higher visitor counts.

### Staffing Recommendations
- **OPD Department**: Deploy 8-10 doctors during peak hours
- **Surgery Department**: Maintain 5-6 surgeons for scheduled procedures
- **Nursing Staff**: Increase by 20% during rush hours

### Inventory Alerts
""" + "\n".join([f"- **{item['item']}**: Stock at {item['stock']} units (Threshold: {item['threshold']})" 
                 for item in data['pharmacy_inventory'] if item['stock'] < item['threshold']]) + """

### Operational Advice
**Key Strategy**: Open additional registration counters at 9:30 AM to handle the morning rush efficiently.

---
*To get AI-powered analysis, please wait a few minutes and try again, or upgrade your API quota.*
"""
            else:
                analysis = f"**Error**: Unable to generate AI analysis. {error_msg}"
        
        return {
            "raw_data": data,
            "analysis": analysis
        }

if __name__ == "__main__":
    hospital_agent = HospitalAgent()
    result = hospital_agent.analyze_situation()
    print("Simulated Data:", result["raw_data"])
    print("\nAgent Analysis:\n", result["analysis"])

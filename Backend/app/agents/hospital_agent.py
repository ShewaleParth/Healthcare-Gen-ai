from app.utils.groq_client import groq_client
from app.config import Config
import random
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

class HospitalAgent:
    """Hospital Operations Optimization Agent using Groq API"""
    
    def __init__(self):
        """Initialize hospital agent"""
        if not groq_client:
            logger.warning("Groq client not initialized - API key may be missing")
        self.client = groq_client

    def simulate_hospital_data(self):
        """Generates simulated hospital data for the current day"""
        current_time = datetime.now()
        
        # Simulate OPD Visits (Time-series data)
        opd_visits = []
        for hour in range(8, 20):  # 8 AM to 8 PM
            visitors = random.randint(10, 50)
            if hour in [10, 11, 17, 18]:  # Peak hours
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
            "surgeries": surgeries,
            "pharmacy_inventory": inventory
        }

    def optimize_hospital_operations(self):
        """Analyzes hospital data and provides optimization recommendations"""
        
        # Get simulated data
        hospital_data = self.simulate_hospital_data()
        
        # Prepare data summary for AI analysis
        data_summary = f"""
**Hospital Operations Data** (Generated: {hospital_data['timestamp']})

**OPD Patient Flow:**
- Total visits today: {sum(v['visitors'] for v in hospital_data['opd_visits'])} patients
- Peak hours: 10:00-11:00 and 17:00-18:00
- Hourly breakdown: {json.dumps(hospital_data['opd_visits'], indent=2)}

**Surgery Schedule:**
{json.dumps(hospital_data['surgeries'], indent=2)}
- Total surgeries scheduled: {sum(s['count'] for s in hospital_data['surgeries'])}

**Pharmacy Inventory Status:**
{json.dumps(hospital_data['pharmacy_inventory'], indent=2)}
- Low stock items: {[item['item'] for item in hospital_data['pharmacy_inventory'] if item['stock'] < item['threshold']]}
"""
        
        system_prompt = """You are an expert Hospital Operations Manager and Optimization AI.
        
Your role:
- Analyze hospital data and identify bottlenecks
- Optimize patient flow and resource allocation
- Predict peak hours and staffing needs
- Manage inventory and prevent stockouts
- Provide actionable, data-driven recommendations

Always prioritize patient safety and operational efficiency."""

        user_prompt = f"""
Analyze the following hospital data and provide comprehensive recommendations:

{data_summary}

**Please provide:**

1. **Patient Flow Optimization**
   - Identify peak hours and bottlenecks
   - Recommend staff allocation for different time slots
   - Suggest strategies to reduce wait times

2. **Surgery Department Efficiency**
   - Analyze surgery load and OR utilization
   - Recommend optimal scheduling
   - Identify potential conflicts or overload

3. **Inventory Management**
   - Flag critical low-stock items
   - Prioritize reordering based on urgency
   - Suggest optimal stock levels

4. **Resource Allocation**
   - Recommend doctor and nurse staffing levels
   - Suggest department-wise resource distribution
   - Identify areas needing immediate attention

5. **Actionable Recommendations**
   - Top 3 immediate actions needed
   - Long-term optimization strategies
   - Risk mitigation measures

Format your response in clear, professional markdown suitable for hospital administrators.
"""
        
        if not self.client:
            # Fallback response when API is not available
            return {
                "analysis": Config.ERROR_MESSAGES["no_api_key"],
                "raw_data": hospital_data,
                "success": False,
                "error": "no_api_key"
            }
        
        try:
            # Call Groq API using centralized client
            response = self.client.chat_completion(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                agent_type="hospital"
            )
            
            if response["success"]:
                # Format the complete response
                formatted_response = f"""
## 🏥 Hospital Operations Optimization Report

**Generated**: {hospital_data['timestamp']}
**Model**: {response['model']}
{' (Fallback)' if response.get('fallback') else ''}

{response['content']}

---
**Analysis Method**: Groq AI ({response['model']})
**Tokens Used**: {response['usage']['total_tokens']}
**Data Source**: Real-time hospital operations simulation
"""
                
                return {
                    "analysis": formatted_response,
                    "raw_data": hospital_data,
                    "success": True,
                    "model_used": response['model'],
                    "tokens_used": response['usage']['total_tokens']
                }
            else:
                # API call failed
                return {
                    "analysis": response.get("message", Config.ERROR_MESSAGES["model_error"]),
                    "raw_data": hospital_data,
                    "success": False,
                    "error": response.get("error", "unknown")
                }
                
        except Exception as e:
            logger.error(f"Hospital optimization failed: {e}")
            return {
                "analysis": f"""
## ⚠️ Hospital Operations Analysis Unavailable

**Error**: {str(e)}

**Troubleshooting**:
1. Check your Groq API key in .env file
2. Verify internet connection
3. Check Groq service status at https://status.groq.com

**Simulated Data Available**:
The system has generated hospital data but cannot provide AI analysis at this time.
Please check the raw data section for current hospital metrics.
""",
                "raw_data": hospital_data,
                "success": False,
                "error": str(e)
            }

if __name__ == "__main__":
    agent = HospitalAgent()
    result = agent.optimize_hospital_operations()
    print(result["analysis"])
    if result["success"]:
        print(f"\n✅ Success! Tokens used: {result['tokens_used']}")
    else:
        print(f"\n❌ Error: {result.get('error', 'Unknown')}")

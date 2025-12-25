from app.util.smart_ai_client import smart_ai_client
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
        self.client = smart_ai_client
        self.system_message = """You are an expert Hospital Operations Manager and Optimization AI.

Your goal is to optimize hospital workflows, reduce waiting times, and manage resources efficiently.

Responsibilities:
- Analyze the provided hospital data (OPD visits, surgery schedules, pharmacy inventory).
- Predict potential rush hours and bottlenecks.
- Recommend optimal staff allocation (doctors, nurses) for different departments.
- Identify inventory shortages and suggest reordering priorities.
- Output your analysis in a structured, actionable format for the hospital dashboard.
- Always prioritize patient safety and operational efficiency.

Provide responses in markdown format for clarity."""

    def simulate_hospital_data(self):
        """Generates comprehensive simulated hospital data for the dashboard."""
        current_time = datetime.now()
        
        # Simulate OPD Visits (Time-series like data)
        opd_visits = []
        total_opd_today = 0
        for hour in range(8, 20): # 8 AM to 8 PM
            visitors = random.randint(10, 50)
            if hour in [10, 11, 17, 18]: # Peak hours
                visitors += random.randint(20, 40)
            opd_visits.append({"hour": f"{hour}:00", "visitors": visitors})
            total_opd_today += visitors

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

        # NEW: KPI Metrics
        total_beds = 250
        occupied_beds = random.randint(150, 230)
        active_emergencies = random.randint(3, 15)
        avg_wait_time = random.randint(15, 45)  # minutes
        critical_alerts = len([i for i in inventory if i['stock'] < i['threshold']])
        
        kpi_metrics = {
            "total_patients_today": total_opd_today + random.randint(20, 50),  # OPD + Admissions
            "active_emergencies": active_emergencies,
            "bed_occupancy_rate": round((occupied_beds / total_beds) * 100, 1),
            "avg_wait_time_mins": avg_wait_time,
            "critical_alerts": critical_alerts
        }

        # NEW: Department Metrics
        departments = [
            {"name": "Cardiology", "patients": random.randint(15, 45), "capacity": 50, "utilization": 0},
            {"name": "Orthopedics", "patients": random.randint(20, 40), "capacity": 45, "utilization": 0},
            {"name": "Pediatrics", "patients": random.randint(25, 50), "capacity": 60, "utilization": 0},
            {"name": "Emergency", "patients": active_emergencies, "capacity": 20, "utilization": 0},
            {"name": "General Medicine", "patients": random.randint(30, 60), "capacity": 70, "utilization": 0},
        ]
        
        for dept in departments:
            dept["utilization"] = round((dept["patients"] / dept["capacity"]) * 100, 1)

        # NEW: Bed Statistics
        bed_stats = {
            "total_beds": total_beds,
            "occupied_beds": occupied_beds,
            "available_beds": total_beds - occupied_beds,
            "icu_beds": {"total": 30, "occupied": random.randint(15, 28)},
            "general_beds": {"total": 180, "occupied": random.randint(100, 170)},
            "emergency_beds": {"total": 40, "occupied": random.randint(10, 35)}
        }

        # NEW: Emergency Room Metrics
        er_metrics = {
            "current_patients": active_emergencies,
            "avg_triage_time_mins": random.randint(5, 15),
            "critical_cases": random.randint(1, 5),
            "stable_cases": active_emergencies - random.randint(1, 5),
            "hourly_arrivals": [
                {"hour": f"{h}:00", "arrivals": random.randint(1, 8)} 
                for h in range(max(0, current_time.hour - 6), current_time.hour + 1)
            ]
        }

        # NEW: Staff Availability
        staff_availability = {
            "doctors": {
                "on_duty": random.randint(25, 40),
                "total": 50,
                "by_department": {
                    "Cardiology": random.randint(4, 8),
                    "Orthopedics": random.randint(3, 6),
                    "Pediatrics": random.randint(5, 9),
                    "Emergency": random.randint(6, 10),
                    "General": random.randint(7, 12)
                }
            },
            "nurses": {
                "on_duty": random.randint(60, 90),
                "total": 120,
                "by_shift": {
                    "morning": random.randint(30, 40),
                    "evening": random.randint(25, 35),
                    "night": random.randint(15, 25)
                }
            },
            "specialists": {
                "available": random.randint(8, 15),
                "total": 20
            }
        }

        # NEW: Historical Trends (Last 7 days)
        historical_trends = {
            "daily_patients": [
                {"day": (current_time - timedelta(days=i)).strftime("%a"), 
                 "patients": random.randint(200, 400)}
                for i in range(6, -1, -1)
            ],
            "daily_emergencies": [
                {"day": (current_time - timedelta(days=i)).strftime("%a"), 
                 "emergencies": random.randint(20, 60)}
                for i in range(6, -1, -1)
            ]
        }

        # NEW: Patient Flow Heatmap Data
        patient_heatmap = []
        departments_list = ["Cardiology", "Orthopedics", "Pediatrics", "Emergency", "General"]
        for hour in range(8, 20):
            for dept in departments_list:
                intensity = random.randint(5, 30)
                if hour in [10, 11, 17, 18]:  # Peak hours
                    intensity += random.randint(10, 20)
                patient_heatmap.append({
                    "hour": f"{hour}:00",
                    "department": dept,
                    "patients": intensity
                })

        return {
            "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "kpi_metrics": kpi_metrics,
            "opd_visits": opd_visits,
            "surgery_schedule": surgeries,
            "pharmacy_inventory": inventory,
            "departments": departments,
            "bed_stats": bed_stats,
            "er_metrics": er_metrics,
            "staff_availability": staff_availability,
            "historical_trends": historical_trends,
            "patient_heatmap": patient_heatmap
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
            # Get response from the Grok client
            response = self.client.simple_prompt(
                prompt=prompt,
                system_message=self.system_message,
                temperature=0.7,
                max_tokens=2048
            )
            analysis = response
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

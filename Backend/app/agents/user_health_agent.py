from app.util.smart_ai_client import smart_ai_client
import random
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class UserHealthAgent:
    def __init__(self):
        self.client = smart_ai_client
        self.system_message = """You are a compassionate AI Health Coach and Personal Medical Assistant.

Your goal is to provide personalized health insights, recommendations, and support to individual patients.

Responsibilities:
- Analyze the patient's health data (vitals, diagnostics, treatments, mental health)
- Calculate overall health scores and identify trends
- Provide personalized health recommendations based on their medical history
- Identify potential health risks and suggest preventive measures
- Offer encouragement and support for treatment adherence
- Suggest lifestyle improvements (diet, exercise, stress management)
- Always prioritize patient safety and well-being

Provide responses in a warm, supportive tone using markdown format."""

    def generate_user_health_data(self, user_id="USER001"):
        """Generates comprehensive simulated health data for a specific user."""
        current_time = datetime.now()
        
        # User Profile
        user_profile = {
            "user_id": user_id,
            "name": "Alex Johnson",
            "age": 35,
            "gender": "Male",
            "blood_group": "A+",
            "height_cm": 175,
            "weight_kg": 75
        }
        
        # Calculate BMI
        bmi = round(user_profile["weight_kg"] / ((user_profile["height_cm"] / 100) ** 2), 1)
        
        # Current Vital Signs
        vitals = {
            "heart_rate": {
                "current": random.randint(65, 85),
                "unit": "bpm",
                "status": "normal",
                "trend": random.choice(["stable", "up", "down"]),
                "history": [
                    {"date": (current_time - timedelta(days=i)).strftime("%Y-%m-%d"), 
                     "value": random.randint(65, 85)}
                    for i in range(6, -1, -1)
                ]
            },
            "blood_pressure": {
                "systolic": random.randint(110, 130),
                "diastolic": random.randint(70, 85),
                "unit": "mmHg",
                "status": "normal",
                "trend": random.choice(["stable", "up", "down"]),
                "history": [
                    {"date": (current_time - timedelta(days=i)).strftime("%Y-%m-%d"), 
                     "systolic": random.randint(110, 130),
                     "diastolic": random.randint(70, 85)}
                    for i in range(6, -1, -1)
                ]
            },
            "temperature": {
                "current": round(random.uniform(97.5, 98.8), 1),
                "unit": "°F",
                "status": "normal"
            },
            "oxygen_saturation": {
                "current": random.randint(96, 100),
                "unit": "%",
                "status": "normal"
            },
            "bmi": {
                "value": bmi,
                "category": "Normal" if 18.5 <= bmi < 25 else ("Underweight" if bmi < 18.5 else "Overweight"),
                "status": "normal" if 18.5 <= bmi < 25 else "attention"
            },
            "blood_glucose": {
                "current": random.randint(80, 110),
                "unit": "mg/dL",
                "status": "normal",
                "fasting": True
            }
        }
        
        # Health Score Calculation
        vitals_score = random.randint(80, 95)
        mental_score = random.randint(70, 85)
        lifestyle_score = random.randint(65, 80)
        overall_score = round((vitals_score + mental_score + lifestyle_score) / 3, 1)
        
        health_score = {
            "overall": overall_score,
            "vitals": vitals_score,
            "mental": mental_score,
            "lifestyle": lifestyle_score,
            "last_updated": current_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Diagnostic History
        diagnostics = [
            {
                "id": "DX003",
                "type": "Chest X-Ray",
                "date": (current_time - timedelta(days=5)).strftime("%Y-%m-%d"),
                "ai_summary": "No abnormalities detected. Lungs are clear with no signs of infection or inflammation.",
                "status": "normal",
                "doctor": "Dr. Sarah Mitchell",
                "department": "Radiology",
                "image_available": True
            },
            {
                "id": "DX002",
                "type": "Blood Test - Complete Panel",
                "date": (current_time - timedelta(days=15)).strftime("%Y-%m-%d"),
                "ai_summary": "All values within normal range. Cholesterol levels are healthy. Vitamin D slightly low - consider supplementation.",
                "status": "attention",
                "doctor": "Dr. James Wilson",
                "department": "Laboratory",
                "results": {
                    "Hemoglobin": "14.5 g/dL",
                    "WBC": "7,200/μL",
                    "Cholesterol": "180 mg/dL",
                    "Vitamin D": "22 ng/mL"
                }
            },
            {
                "id": "DX001",
                "type": "ECG",
                "date": (current_time - timedelta(days=45)).strftime("%Y-%m-%d"),
                "ai_summary": "Normal sinus rhythm. No arrhythmias detected. Heart function is normal.",
                "status": "normal",
                "doctor": "Dr. Emily Chen",
                "department": "Cardiology"
            }
        ]
        
        # Active Treatments
        treatments = [
            {
                "id": "TX002",
                "medication": "Vitamin D3",
                "dosage": "2000 IU",
                "frequency": "Once daily",
                "start_date": (current_time - timedelta(days=10)).strftime("%Y-%m-%d"),
                "duration_days": 90,
                "days_completed": 10,
                "adherence": 90,
                "next_dose": (current_time + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M"),
                "purpose": "Vitamin D deficiency",
                "status": "active"
            },
            {
                "id": "TX001",
                "medication": "Multivitamin",
                "dosage": "1 tablet",
                "frequency": "Once daily",
                "start_date": (current_time - timedelta(days=60)).strftime("%Y-%m-%d"),
                "duration_days": 365,
                "days_completed": 60,
                "adherence": 95,
                "next_dose": (current_time + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M"),
                "purpose": "General wellness",
                "status": "active"
            }
        ]
        
        # Appointments
        appointments = {
            "upcoming": [
                {
                    "id": "APT002",
                    "date": (current_time + timedelta(days=7)).strftime("%Y-%m-%d"),
                    "time": "10:30 AM",
                    "doctor": "Dr. Sarah Mitchell",
                    "department": "Radiology",
                    "type": "Follow-up",
                    "reason": "Review X-ray results",
                    "location": "Building A, Room 203"
                },
                {
                    "id": "APT003",
                    "date": (current_time + timedelta(days=30)).strftime("%Y-%m-%d"),
                    "time": "2:00 PM",
                    "doctor": "Dr. James Wilson",
                    "department": "General Medicine",
                    "type": "Routine Checkup",
                    "reason": "Quarterly health review",
                    "location": "Building B, Room 105"
                }
            ],
            "past": [
                {
                    "id": "APT001",
                    "date": (current_time - timedelta(days=15)).strftime("%Y-%m-%d"),
                    "time": "11:00 AM",
                    "doctor": "Dr. James Wilson",
                    "department": "Laboratory",
                    "type": "Blood Test",
                    "notes": "Routine blood work completed. Results reviewed."
                }
            ]
        }
        
        # Mental Health Tracking
        mental_health = {
            "wellness_score": mental_score,
            "mood_logs": [
                {
                    "date": (current_time - timedelta(days=i)).strftime("%Y-%m-%d"),
                    "mood": random.choice(["Great", "Good", "Okay", "Low"]),
                    "score": random.randint(6, 10)
                }
                for i in range(6, -1, -1)
            ],
            "therapy_sessions": [
                {
                    "date": (current_time - timedelta(days=10)).strftime("%Y-%m-%d"),
                    "therapist": "Dr. Lisa Anderson",
                    "type": "Cognitive Behavioral Therapy",
                    "duration_mins": 50,
                    "notes": "Discussed stress management techniques"
                }
            ],
            "mindfulness_minutes": random.randint(100, 300),
            "last_session": (current_time - timedelta(days=10)).strftime("%Y-%m-%d")
        }
        
        # Health Timeline (Combined view of all medical events)
        timeline = []
        
        # Add diagnostics to timeline
        for diag in diagnostics:
            timeline.append({
                "date": diag["date"],
                "type": "diagnostic",
                "title": diag["type"],
                "description": diag["ai_summary"][:100] + "...",
                "status": diag["status"],
                "icon": "🔬"
            })
        
        # Add treatments to timeline
        for treat in treatments:
            timeline.append({
                "date": treat["start_date"],
                "type": "treatment",
                "title": f"Started {treat['medication']}",
                "description": f"{treat['dosage']} - {treat['frequency']}",
                "status": "active",
                "icon": "💊"
            })
        
        # Add appointments to timeline
        for apt in appointments["past"]:
            timeline.append({
                "date": apt["date"],
                "type": "appointment",
                "title": f"{apt['type']} - {apt['doctor']}",
                "description": apt.get("notes", ""),
                "status": "completed",
                "icon": "📅"
            })
        
        # Add mental health sessions
        for session in mental_health["therapy_sessions"]:
            timeline.append({
                "date": session["date"],
                "type": "mental_health",
                "title": session["type"],
                "description": session["notes"],
                "status": "completed",
                "icon": "🧠"
            })
        
        # Sort timeline by date (most recent first)
        timeline.sort(key=lambda x: x["date"], reverse=True)
        
        # 30-Day Health Trends
        health_trends = {
            "weight": [
                {
                    "date": (current_time - timedelta(days=i*3)).strftime("%Y-%m-%d"),
                    "value": round(75 + random.uniform(-1, 1), 1)
                }
                for i in range(9, -1, -1)
            ],
            "blood_pressure_systolic": [
                {
                    "date": (current_time - timedelta(days=i*3)).strftime("%Y-%m-%d"),
                    "value": random.randint(110, 130)
                }
                for i in range(9, -1, -1)
            ],
            "activity_minutes": [
                {
                    "date": (current_time - timedelta(days=i*3)).strftime("%Y-%m-%d"),
                    "value": random.randint(20, 60)
                }
                for i in range(9, -1, -1)
            ],
            "sleep_hours": [
                {
                    "date": (current_time - timedelta(days=i*3)).strftime("%Y-%m-%d"),
                    "value": round(random.uniform(6.5, 8.5), 1)
                }
                for i in range(9, -1, -1)
            ]
        }
        
        # Alerts and Notifications
        alerts = []
        
        # Check for low vitamin D
        if any(d["type"] == "Blood Test - Complete Panel" and d["status"] == "attention" for d in diagnostics):
            alerts.append({
                "type": "attention",
                "title": "Vitamin D Levels Low",
                "message": "Your recent blood test showed low Vitamin D. Continue taking supplements as prescribed.",
                "action": "View Results",
                "priority": "medium"
            })
        
        # Upcoming appointment reminder
        if appointments["upcoming"]:
            next_apt = appointments["upcoming"][0]
            alerts.append({
                "type": "info",
                "title": "Upcoming Appointment",
                "message": f"You have an appointment with {next_apt['doctor']} on {next_apt['date']} at {next_apt['time']}",
                "action": "View Details",
                "priority": "high"
            })
        
        # Medication adherence
        if any(t["adherence"] < 80 for t in treatments):
            alerts.append({
                "type": "warning",
                "title": "Medication Adherence",
                "message": "Remember to take your medications on time for best results.",
                "action": "Set Reminder",
                "priority": "medium"
            })
        
        return {
            "user_profile": user_profile,
            "health_score": health_score,
            "vitals": vitals,
            "diagnostics": diagnostics,
            "treatments": treatments,
            "appointments": appointments,
            "mental_health": mental_health,
            "timeline": timeline,
            "health_trends": health_trends,
            "alerts": alerts,
            "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def generate_ai_insights(self, health_data):
        """Generate personalized AI health insights and recommendations."""
        
        user_profile = health_data["user_profile"]
        health_score = health_data["health_score"]
        vitals = health_data["vitals"]
        diagnostics = health_data["diagnostics"]
        treatments = health_data["treatments"]
        
        prompt = f"""
        Analyze this patient's health data and provide personalized insights:
        
        **Patient Profile:**
        - Name: {user_profile['name']}
        - Age: {user_profile['age']}
        - Gender: {user_profile['gender']}
        - BMI: {vitals['bmi']['value']} ({vitals['bmi']['category']})
        
        **Health Scores:**
        - Overall: {health_score['overall']}/100
        - Vitals: {health_score['vitals']}/100
        - Mental Health: {health_score['mental']}/100
        - Lifestyle: {health_score['lifestyle']}/100
        
        **Current Vitals:**
        - Heart Rate: {vitals['heart_rate']['current']} bpm ({vitals['heart_rate']['trend']})
        - Blood Pressure: {vitals['blood_pressure']['systolic']}/{vitals['blood_pressure']['diastolic']} mmHg ({vitals['blood_pressure']['trend']})
        - Blood Glucose: {vitals['blood_glucose']['current']} mg/dL
        
        **Recent Diagnostics:**
        {chr(10).join([f"- {d['type']} ({d['date']}): {d['ai_summary']}" for d in diagnostics[:3]])}
        
        **Active Treatments:**
        {chr(10).join([f"- {t['medication']} ({t['dosage']}) - Adherence: {t['adherence']}%" for t in treatments])}
        
        Provide a warm, supportive health report with:
        1. **Overall Health Assessment** - Brief summary of their current health status
        2. **Key Strengths** - What they're doing well
        3. **Areas for Improvement** - Gentle suggestions (2-3 items)
        4. **Personalized Recommendations** - Specific, actionable advice (3-4 items)
        5. **Encouragement** - Positive, motivating message
        
        Keep it concise, supportive, and actionable. Use markdown formatting.
        """
        
        try:
            response = self.client.simple_prompt(
                prompt=prompt,
                system_message=self.system_message,
                temperature=0.7,
                max_tokens=1500
            )
            return response
        except Exception as e:
            # Fallback response
            return f"""
## 🌟 Your Personal Health Report

### Overall Health Assessment
Your health score of **{health_score['overall']}/100** indicates you're in good health! Your vitals are stable, and you're actively managing your health with regular checkups and treatments.

### 💪 Key Strengths
- **Excellent Vital Signs**: Your heart rate and blood pressure are within healthy ranges
- **Proactive Care**: You're staying on top of appointments and diagnostic tests
- **Good Medication Adherence**: {treatments[0]['adherence']}% adherence shows great commitment

### 🎯 Areas for Improvement
- **Vitamin D Levels**: Continue your supplementation as prescribed
- **Physical Activity**: Consider increasing daily movement to 30+ minutes
- **Sleep Quality**: Aim for consistent 7-8 hours of quality sleep

### 📋 Personalized Recommendations
1. **Continue Vitamin D Supplementation**: Your levels are improving - keep it up!
2. **Stay Hydrated**: Aim for 8 glasses of water daily
3. **Regular Exercise**: 30 minutes of moderate activity, 5 days a week
4. **Stress Management**: Practice mindfulness or meditation for 10 minutes daily

### 💙 Keep Up the Great Work!
You're doing an excellent job managing your health. Your consistent approach to medications and regular checkups shows real dedication. Keep up these healthy habits!

---
*Next checkup: {health_data['appointments']['upcoming'][0]['date']} with {health_data['appointments']['upcoming'][0]['doctor']}*
"""

if __name__ == "__main__":
    agent = UserHealthAgent()
    health_data = agent.generate_user_health_data()
    print("User Health Data Generated:")
    print(f"Health Score: {health_data['health_score']['overall']}/100")
    print(f"Vitals: {health_data['vitals']['heart_rate']['current']} bpm")
    print(f"Diagnostics: {len(health_data['diagnostics'])} records")

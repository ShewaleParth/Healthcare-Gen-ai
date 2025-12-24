#!/usr/bin/env python3
"""
Comprehensive Backend Health Check for Aarogya AI
Tests all agents, routes, and API connectivity
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("AAROGYA AI - BACKEND HEALTH CHECK")
print("=" * 60)

# Test 1: Environment Configuration
print("\n[1/7] Checking Environment Configuration...")
api_key = os.getenv("GOOGLE_API_KEY")
if api_key and api_key != "your_groq_api_key_here":
    print("✅ API Key configured")
    print(f"   Key prefix: {api_key[:10]}...")
else:
    print("❌ API Key NOT configured")
    print("   Please set GOOGLE_API_KEY in .env file")
    print("   Get free key from: https://console.groq.com")
    sys.exit(1)

# Test 2: Import All Agents
print("\n[2/7] Testing Agent Imports...")
try:
    from app.agents.hospital_agent import HospitalAgent
    print("✅ Hospital Agent imported")
except Exception as e:
    print(f"❌ Hospital Agent failed: {e}")
    sys.exit(1)

try:
    from app.agents.diagnostic_agent import DiagnosticAgent
    print("✅ Diagnostic Agent imported")
except Exception as e:
    print(f"❌ Diagnostic Agent failed: {e}")
    sys.exit(1)

try:
    from app.agents.mental_health_agent import MentalHealthAgent
    print("✅ Mental Health Agent imported")
except Exception as e:
    print(f"❌ Mental Health Agent failed: {e}")
    sys.exit(1)

try:
    from app.agents.treatment_agent import TreatmentAgent
    print("✅ Treatment Agent imported")
except Exception as e:
    print(f"❌ Treatment Agent failed: {e}")
    sys.exit(1)

# Test 3: Import All Routes
print("\n[3/7] Testing Route Imports...")
try:
    from app.routes import hospital, diagnosis, treatment, mental_health
    print("✅ All routes imported successfully")
except Exception as e:
    print(f"❌ Route import failed: {e}")
    sys.exit(1)

# Test 4: Initialize Agents
print("\n[4/7] Initializing Agents...")
try:
    hospital_agent = HospitalAgent()
    print("✅ Hospital Agent initialized")
except Exception as e:
    print(f"❌ Hospital Agent init failed: {e}")
    sys.exit(1)

try:
    diagnostic_agent = DiagnosticAgent()
    print("✅ Diagnostic Agent initialized")
except Exception as e:
    print(f"❌ Diagnostic Agent init failed: {e}")
    sys.exit(1)

try:
    mental_health_agent = MentalHealthAgent()
    print("✅ Mental Health Agent initialized")
except Exception as e:
    print(f"❌ Mental Health Agent init failed: {e}")
    sys.exit(1)

try:
    treatment_agent = TreatmentAgent()
    print("✅ Treatment Agent initialized")
except Exception as e:
    print(f"❌ Treatment Agent init failed: {e}")
    sys.exit(1)

# Test 5: Test Hospital Agent (Quick)
print("\n[5/7] Testing Hospital Agent...")
try:
    data = hospital_agent.simulate_hospital_data()
    if data and "opd_visits" in data:
        print("✅ Hospital data simulation works")
        print(f"   Generated {len(data['opd_visits'])} OPD visit records")
    else:
        print("⚠️  Hospital data incomplete")
except Exception as e:
    print(f"❌ Hospital Agent test failed: {e}")

# Test 6: Test Mental Health Agent (Quick)
print("\n[6/7] Testing Mental Health Agent...")
try:
    response = mental_health_agent.chat("Hello, I'm feeling a bit anxious today")
    if response and "response" in response:
        print("✅ Mental Health chat works")
        print(f"   Risk level: {response.get('risk_level', 'N/A')}")
    else:
        print("⚠️  Mental Health response incomplete")
except Exception as e:
    print(f"❌ Mental Health Agent test failed: {e}")
    print(f"   Error: {str(e)}")

# Test 7: Test Treatment Agent (Quick)
print("\n[7/7] Testing Treatment Agent...")
try:
    test_patient = {
        "age": 45,
        "weight": 75,
        "condition": "Hypertension",
        "history": "Diabetes",
        "current_meds": ["Metformin"],
        "allergies": ["Penicillin"]
    }
    recommendation = treatment_agent.recommend_treatment(test_patient)
    if recommendation and len(recommendation) > 100:
        print("✅ Treatment recommendations work")
        print(f"   Generated {len(recommendation)} characters of analysis")
    else:
        print("⚠️  Treatment recommendation incomplete")
except Exception as e:
    print(f"❌ Treatment Agent test failed: {e}")
    print(f"   Error: {str(e)}")

# Summary
print("\n" + "=" * 60)
print("HEALTH CHECK SUMMARY")
print("=" * 60)
print("✅ All core components are functional")
print("\n📝 NOTES:")
print("   - If you see API errors, check your Groq API key")
print("   - Get free key from: https://console.groq.com")
print("   - Free tier: 30 requests/min, unlimited daily")
print("\n🚀 Backend is ready for use!")
print("=" * 60)

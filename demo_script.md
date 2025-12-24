# Aarogya Demo Script - 3 Minutes

## Setup (Before Demo)
- ✅ Backend running: `cd Backend && python -m uvicorn app.main:app --reload`
- ✅ Frontend running: `cd Frontend && npm run dev`
- ✅ Browser open to `http://localhost:5173`
- ✅ Have this script visible on second screen

---

## Demo Flow (3 minutes)

### [0:00-0:30] Introduction & Dashboard
**What to say:**
> "Hi! I'm presenting Aarogya - an AI-powered hospital intelligence system built with Google's Gemini and Vertex AI. Unlike traditional single-model approaches, we use a multi-agent architecture where specialized AI agents handle different healthcare domains."

**Actions:**
1. Show Dashboard page
2. Point to Impact Metrics at top
3. Highlight the numbers: "1,247 patients analyzed, 2.3 second response time, 3 crisis interventions today"
4. Scroll to hospital operations charts
5. Click "Refresh Analysis"

**What to say:**
> "Our Hospital Operations Agent analyzes patient flow, surgery schedules, and inventory in real-time, providing actionable recommendations to reduce wait times."

---

### [0:30-1:00] Diagnostic Agent
**What to say:**
> "Let me show you our Diagnostic Agent, which combines Vertex AI Vision with Gemini for medical image analysis."

**Actions:**
1. Navigate to "AI Diagnostics"
2. Click "Chest X-Ray - Pneumonia Detection" demo button
3. Wait for image to load
4. Click "Run Diagnostic Analysis"
5. While loading, say: "This agent provides doctor-friendly explanations, not just predictions"
6. Show the analysis results

**What to say:**
> "Notice the structured findings, confidence level, and most importantly - the medical disclaimer. We always emphasize that AI assists, but doesn't replace, medical professionals."

---

### [1:00-1:30] Treatment Safety Agent
**What to say:**
> "Our Treatment Agent goes beyond recommendations - it actively detects drug interactions and safety risks."

**Actions:**
1. Navigate to "Treatment & Safety"
2. Click "Hypertension with Diabetes" demo button
3. Show the pre-filled form (point out the Penicillin allergy)
4. Click "Generate Treatment Plan"
5. Show the safety warnings

**What to say:**
> "See how it detected the allergy and provided safer alternatives? This kind of safety checking can prevent medication errors that affect millions of patients annually."

---

### [1:30-2:30] Mental Health Companion (STAR FEATURE)
**What to say:**
> "This is our most innovative feature - a Mental Health Companion with built-in crisis detection. This is genuinely unique in healthcare AI."

**Actions:**
1. Navigate to "Mental Health"
2. Point to the Risk Indicator showing "Low Risk"
3. Click "Load Anxiety Demo" button
4. Click Send
5. Show the supportive CBT-based response
6. Now click "Load Crisis Demo" button
7. Click Send
8. **WAIT for emergency protocol to activate**
9. Show the full-screen red emergency overlay

**What to say:**
> "This is our 3-tier risk assessment system in action. When critical keywords are detected, we immediately activate emergency protocols with hotline numbers and escalate to human professionals. This isn't just a chatbot - it's a safety system that could save lives."

**Actions:**
10. Close the emergency overlay
11. Point to the risk indicator now showing "CRITICAL"

---

### [2:30-3:00] Wrap-up & Impact
**What to say:**
> "So to recap - Aarogya uses four specialized AI agents working together: Diagnostics, Treatment Safety, Mental Health, and Hospital Operations. What makes this special is our safety-first approach: we have medical disclaimers, data anonymization, crisis detection, and human escalation built into every layer."

**Actions:**
1. Navigate back to Dashboard
2. Show Impact Metrics one more time

**What to say:**
> "This system is designed to scale to thousands of hospitals, bringing specialist-level AI assistance to underserved areas while maintaining the highest safety standards. We're not replacing doctors - we're empowering them with AI that they can trust."

**Final line:**
> "Thank you! I'm happy to answer any questions about our architecture, safety features, or implementation."

---

## Backup Scenarios (If Something Fails)

### If Backend is Down:
- Show the simulated/fallback responses
- Explain: "We have graceful degradation - if APIs fail, the system falls back to simulated data rather than crashing"

### If Demo Buttons Don't Work:
- Manually type in the demo data
- For Mental Health: Type "I don't see the point in going on anymore"

### If Judges Ask Technical Questions:
**Q: How do you ensure AI accuracy?**
> "We use Gemini 2.0 Flash for reasoning and Vertex AI Vision for specialized medical imaging. Every output includes confidence scores and disclaimers. In production, we'd validate against labeled medical datasets."

**Q: What about data privacy?**
> "We use SHA-256 hashing for patient IDs, encrypted transmission, and BigQuery for secure analytics. All data handling follows HIPAA-compliant patterns."

**Q: How would this scale?**
> "Cloud-native architecture on GCP. Each agent can scale independently. We use Cloud Run for serverless deployment and Cloud Storage for medical images."

**Q: What's your plan for regulatory approval?**
> "This is a clinical decision support tool, not a diagnostic device, so it falls under different regulations. We'd work with medical professionals for validation and pursue FDA clearance for the diagnostic component."

---

## Key Points to Emphasize

1. **Multi-agent architecture** (not just a single model)
2. **Mental health crisis detection** (unique differentiator)
3. **Safety-first design** (disclaimers, risk detection, human escalation)
4. **Production-ready thinking** (fallbacks, error handling, security)
5. **Real-world impact** (underserved areas, medication safety, crisis intervention)

---

## Time Checkpoints

- ✅ 0:30 - Should be on Diagnostics page
- ✅ 1:00 - Should be on Treatment page
- ✅ 1:30 - Should be on Mental Health page
- ✅ 2:30 - Should be wrapping up on Dashboard

**If running over time:** Skip the Treatment demo and go straight from Diagnostics to Mental Health.

**If running under time:** Add more detail about the multi-agent architecture and how agents could collaborate on a single patient case.

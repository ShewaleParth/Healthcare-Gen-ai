# Aarogya - AI-Powered Hospital Intelligence System

> **GenAI Hackathon Mumbai 2024** - Multi-Agent Healthcare Solution using Google's AI Development Kit (ADK)

Aarogya is an advanced AI system designed to optimize hospital workflows and provide intelligent medical assistance. It leverages **Google Gemini**, **Vertex AI**, and **BigQuery** to solve critical healthcare challenges through a multi-agent architecture.

## 🎯 Problem Statement

Healthcare systems face critical challenges:
- **Diagnostic Delays**: Limited specialist access in rural/underserved areas
- **Treatment Safety**: Risk of drug interactions and dosage errors
- **Mental Health Crisis**: Lack of immediate support for patients in distress
- **Operational Inefficiency**: Poor resource allocation leading to bottlenecks

## 💡 Solution Overview

Aarogya implements a **multi-agent ADK architecture** with four specialized AI agents:

### 1. 🩻 Diagnostic Agent
- **Technology**: Vertex AI Vision + Gemini 2.0 Flash
- **Function**: Analyzes medical images (X-rays, MRIs, retinal scans)
- **Output**: Doctor-friendly explanations with confidence scores
- **Safety**: Always includes medical professional disclaimer

### 2. 💊 Personalized Care Agent
- **Technology**: Gemini 2.0 Flash + BigQuery
- **Function**: Recommends treatment plans based on patient vitals and EHR
- **Safety Layer**: Drug interaction detection, allergy checking, overdose prevention
- **Output**: Dosage recommendations with safer alternatives

### 3. 🧠 Mental Health Companion
- **Technology**: Gemini 2.0 Flash + ADK Risk Monitoring
- **Function**: Compassionate conversational support with CBT techniques
- **Safety**: 3-tier risk assessment with emergency protocol escalation
- **Output**: Supportive responses with crisis intervention when needed

### 4. 🏥 Hospital Operations Agent
- **Technology**: Vertex AI Forecasting + Gemini Reasoning
- **Function**: Predicts patient flow and optimizes resource allocation
- **Output**: Rush hour predictions, staffing recommendations, inventory alerts

## 🏗️ Architecture

```
Frontend (React) → FastAPI Backend → Multi-Agent System (ADK)
                                            ↓
                            ┌───────────────┴───────────────┐
                            │                               │
                    Vertex AI (Vision/Forecast)    Gemini 2.0 Flash
                            │                               │
                    ┌───────┴───────┐               ┌───────┴───────┐
                BigQuery          Cloud Storage
            (Patient Records)   (Medical Images)
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed system design.

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.13)
- **Agent Framework**: Agno (Google ADK wrapper)
- **AI Models**: 
  - Gemini 2.0 Flash (multimodal reasoning)
  - Vertex AI Vision (medical imaging)
  - Vertex AI Forecasting (hospital operations)
- **Database**: BigQuery (patient records & analytics)
- **Storage**: Cloud Storage (medical images)

### Frontend
- **Framework**: React 18 + Vite
- **Styling**: Tailwind CSS
- **Charts**: Recharts (data visualization)
- **Routing**: React Router DOM
- **Markdown**: react-markdown (AI report rendering)

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Node.js 18+
- Google Cloud Account (for Vertex AI & BigQuery)
- Google AI Studio API Key

### 1. Clone Repository
```bash
git clone <repository-url>
cd "Gen Ai Hackathon"
```

### 2. Backend Setup

#### Install Dependencies
```bash
cd Backend
pip install -r ../requirements.txt
```

#### Configure Environment Variables
Create/edit `.env` file in the project root:
```env
# Google AI Studio API Key (Required)
GOOGLE_API_KEY=your-api-key-here

# Vertex AI Configuration (Optional for MVP, Required for Production)
GCP_PROJECT_ID=your-gcp-project-id
GCP_LOCATION=us-central1

# BigQuery Configuration (Optional)
BIGQUERY_DATASET=aarogya_healthcare

# Cloud Storage (Optional)
GCS_BUCKET=aarogya-medical-data
```

**Get your API key**: https://aistudio.google.com/

#### Run Backend Server
```bash
python -m uvicorn app.main:app --reload
```

Backend will be available at: `http://127.0.0.1:8000`

### 3. Frontend Setup

#### Install Dependencies
```bash
cd Frontend
npm install
```

#### Run Development Server
```bash
npm run dev
```

Frontend will be available at: `http://localhost:5173`

## 📱 Using the Application

### Dashboard (Hospital Operations)
1. Navigate to `http://localhost:5173`
2. View real-time hospital metrics:
   - OPD patient flow (Area Chart)
   - Surgery distribution (Pie Chart)
   - Low stock pharmacy alerts
3. Click "Refresh Analysis" for AI-generated optimization report

### AI Diagnostics
1. Click "AI Diagnostics" in sidebar
2. Upload medical image (X-ray, MRI, etc.)
3. View AI analysis with:
   - Primary findings
   - Potential diagnosis
   - Confidence level
   - Clinical recommendations

### Treatment & Safety
1. Click "Treatment & Safety" in sidebar
2. Enter patient details:
   - Age, weight, medical condition
   - Medical history
   - Current medications
   - Known allergies
3. Get AI-powered recommendations:
   - Optimal dosage
   - Alternative medicines
   - Safety warnings (interactions, allergies)

### Mental Health Companion
1. Click "Mental Health" in sidebar
2. Start conversation with AI companion
3. Receive:
   - Compassionate, non-judgmental support
   - CBT-guided coping strategies
   - Emergency protocol if crisis detected

## 🔐 Security & Privacy

### HIPAA Compliance Measures
- ✅ **Data Anonymization**: SHA-256 hashing of patient IDs
- ✅ **Encrypted Transmission**: HTTPS for all API calls
- ✅ **Access Control**: API authentication (production)
- ✅ **Audit Logging**: BigQuery event tracking
- ✅ **Emergency Protocols**: Crisis intervention for mental health

### Data Handling
```python
# Patient data is anonymized before storage
patient_id → SHA256 → anonymized_hash
# Only aggregated, de-identified data used for analytics
```

## 🧪 Testing

### Manual Testing Scenarios

#### 1. Diagnostic Agent
- Upload sample X-ray image
- Verify analysis includes findings, diagnosis, confidence
- Check for medical disclaimer

#### 2. Treatment Agent
- Input patient: Age=45, Weight=75kg, Condition=Hypertension
- Add allergy: Penicillin
- Verify safety warnings appear

#### 3. Mental Health Agent
- Send message: "I feel anxious"
- Verify supportive CBT response
- Send message: "I want to hurt myself"
- Verify emergency protocol activation

#### 4. Hospital Operations
- Click "Refresh Analysis" on dashboard
- Verify charts update with new data
- Check AI report for staffing recommendations

## 📊 API Documentation

Once backend is running, visit:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### Key Endpoints
- `POST /api/v1/diagnostic/analyze-image` - Medical image analysis
- `POST /api/v1/treatment/recommend-treatment` - Treatment recommendations
- `POST /api/v1/mental-health/chat` - Mental health conversation
- `POST /api/v1/hospital/optimize` - Hospital operations optimization

## 🎯 MVP Scope (6-Hour Hackathon)

### ✅ Implemented
- Multi-agent ADK architecture
- All 4 agents with Gemini integration
- Vertex AI Vision integration (with fallback)
- BigQuery service layer (with fallback)
- Risk detection & emergency protocols
- Beautiful, responsive UI with charts
- Complete data flow architecture

### 🔄 Production Enhancements
- Full Vertex AI Forecasting integration
- Real EHR system integration
- Advanced sentiment analysis for mental health
- Cloud deployment (Cloud Run + Cloud Storage)
- Comprehensive audit logging
- Multi-language support

## 🏆 Hackathon Highlights

### Innovation
- **Multi-Agent ADK Design**: Specialized agents for each healthcare domain
- **Responsible AI**: Safety-first with disclaimers, risk detection, human escalation
- **Explainable AI**: Clear reasoning, not just predictions
- **Hybrid Approach**: Vertex AI (specialized) + Gemini (generalist)

### Technical Excellence
- **Scalable Architecture**: Cloud-native design with GCP services
- **Graceful Degradation**: Fallback mechanisms for API limits
- **Security First**: HIPAA-compliant data handling
- **Production-Ready**: Complete with error handling, logging, monitoring hooks

### Real-World Impact
- **Accessibility**: Brings specialist-level diagnostics to underserved areas
- **Safety**: Prevents medication errors through AI-powered safety checks
- **Mental Health**: Provides immediate support with crisis intervention
- **Efficiency**: Optimizes hospital operations to reduce wait times

## 📄 Documentation

- [ARCHITECTURE.md](./ARCHITECTURE.md) - Detailed system architecture
- [SOLUTION_ALIGNMENT.md](./SOLUTION_ALIGNMENT.md) - Gap analysis & alignment
- [API Documentation](http://127.0.0.1:8000/docs) - Interactive API docs

## 🤝 Team

Built for **GenAI Hackathon Mumbai 2024**

## 📜 License

Hackathon Project - Open Source

## 🙏 Acknowledgments

- Google Cloud Platform for Vertex AI & BigQuery
- Google AI Studio for Gemini API
- Agno framework for ADK integration
- Healthcare professionals for domain guidance

---

**⚠️ Important Disclaimer**: This is a hackathon MVP demonstrating AI capabilities in healthcare. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare professionals for medical decisions.

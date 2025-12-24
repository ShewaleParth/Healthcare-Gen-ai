# Aarogya - Quick Setup Guide

## 📋 Prerequisites

Before you begin, ensure you have:
- **Python 3.13+** installed
- **Node.js 18+** and npm installed
- **Google AI Studio API Key** (get from https://aistudio.google.com/)
- Git (for cloning the repository)

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Clone & Navigate
```bash
cd d:\aarogya\Healthcare-Gen-ai
```

### Step 2: Backend Setup

#### Install Python Dependencies
```bash
pip install -r requirements.txt
```

**Dependencies Installed:**
- `fastapi` - Modern web framework
- `uvicorn` - ASGI server
- `agno` - Google ADK wrapper
- `google-generativeai` - Gemini API
- `google-cloud-aiplatform` - Vertex AI
- `google-cloud-bigquery` - BigQuery analytics
- `google-cloud-storage` - Cloud storage
- `pydantic` - Data validation
- `python-multipart` - File upload support
- `requests` - HTTP library
- `python-dotenv` - Environment variables
- `pillow` - Image processing
- `numpy` - Numerical computing
- `pandas` - Data analysis

#### Configure Environment Variables
Create a `.env` file in the project root:
```env
# Required - Get from https://aistudio.google.com/
GOOGLE_API_KEY=your-api-key-here

# Optional - For Vertex AI (production)
GCP_PROJECT_ID=your-gcp-project-id
GCP_LOCATION=us-central1

# Optional - For BigQuery
BIGQUERY_DATASET=aarogya_healthcare

# Optional - For Cloud Storage
GCS_BUCKET=aarogya-medical-data
```

#### Start Backend Server
```bash
cd Backend
python -m uvicorn app.main:app --reload
```

Backend will run at: `http://127.0.0.1:8000`

---

### Step 3: Frontend Setup

#### Install Node.js Dependencies
```bash
cd Frontend
npm install
```

**Dependencies Installed:**
- `react` (18.3.1) - UI library
- `react-dom` (18.3.1) - React DOM renderer
- `react-router-dom` (6.22.3) - Routing
- `react-markdown` (9.0.1) - Markdown rendering
- `react-hot-toast` (2.6.0) - Toast notifications ✨ NEW
- `react-transition-group` (4.4.5) - Animations ✨ NEW
- `recharts` (2.12.3) - Charts
- `lucide-react` (0.363.0) - Icons
- `vite` (5.4.21) - Build tool
- `tailwindcss` (3.4.4) - CSS framework
- `autoprefixer` (10.4.19) - CSS processing
- `postcss` (8.4.38) - CSS processing

#### Start Frontend Dev Server
```bash
npm run dev
```

Frontend will run at: `http://localhost:5173`

---

## ✅ Verify Installation

### Check Backend
1. Open browser to `http://127.0.0.1:8000`
2. You should see: `{"status":"running","message":"GenAI Hackathon Backend is live"}`
3. Visit `http://127.0.0.1:8000/docs` for API documentation

### Check Frontend
1. Open browser to `http://localhost:5173`
2. You should see the Aarogya Dashboard
3. Impact Metrics should be visible at the top
4. Charts should load with hospital data

---

## 🎯 Quick Test (2 Minutes)

### Test 1: Dashboard
1. Navigate to Dashboard (should load automatically)
2. Click "Refresh Analysis" button
3. ✅ Toast notification appears
4. ✅ Charts update

### Test 2: Diagnostics
1. Click "AI Diagnostics" in sidebar
2. Click "Chest X-Ray - Pneumonia Detection" demo button
3. ✅ Image loads
4. Click "Run Diagnostic Analysis"
5. ✅ Analysis appears

### Test 3: Mental Health (CRITICAL!)
1. Click "Mental Health" in sidebar
2. Click "Load Crisis Demo" button
3. Click "Send"
4. ✅ Emergency protocol overlay appears (red screen)
5. ✅ Hotline numbers displayed

---

## 🐛 Troubleshooting

### Backend Issues

**Error: "No module named 'agno'"**
```bash
pip install agno
```

**Error: "GOOGLE_API_KEY not found"**
- Create `.env` file in project root
- Add: `GOOGLE_API_KEY=your-key-here`
- Get key from: https://aistudio.google.com/

**Error: "Port 8000 already in use"**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
python -m uvicorn app.main:app --reload --port 8001
```

### Frontend Issues

**Error: "Cannot find module 'react-hot-toast'"**
```bash
cd Frontend
npm install react-hot-toast react-transition-group
```

**Error: "Port 5173 already in use"**
```bash
# Kill the process or Vite will auto-select next available port
```

**Error: "Failed to fetch" in browser console**
- Ensure backend is running on `http://127.0.0.1:8000`
- Check CORS settings in `Backend/app/main.py`

---

## 📦 Complete Dependency List

### Backend (Python)
```txt
fastapi
uvicorn
agno
google-generativeai
google-cloud-aiplatform
google-cloud-bigquery
google-cloud-storage
pydantic
python-multipart
requests
python-dotenv
pillow
numpy
pandas
```

### Frontend (Node.js)
```json
{
  "dependencies": {
    "lucide-react": "^0.363.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-hot-toast": "^2.6.0",
    "react-markdown": "^9.0.1",
    "react-router-dom": "^6.22.3",
    "react-transition-group": "^4.4.5",
    "recharts": "^2.12.3"
  },
  "devDependencies": {
    "@types/react": "^18.3.3",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.1",
    "autoprefixer": "^10.4.19",
    "eslint": "^8.57.0",
    "eslint-plugin-react": "^7.34.2",
    "eslint-plugin-react-hooks": "^4.6.2",
    "eslint-plugin-react-refresh": "^0.4.7",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.4",
    "vite": "^5.4.21"
  }
}
```

---

## 🎬 Ready for Demo!

Once both servers are running:

1. **Open**: `http://localhost:5173`
2. **Follow**: `demo_script.md` for 3-minute walkthrough
3. **Emphasize**: Mental health crisis detection (your killer feature!)

---

## 🔧 Development Commands

### Backend
```bash
# Start server
cd Backend
python -m uvicorn app.main:app --reload

# Start with different port
python -m uvicorn app.main:app --reload --port 8001

# View API docs
# Open: http://127.0.0.1:8000/docs
```

### Frontend
```bash
# Start dev server
cd Frontend
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

---

## 📝 Environment Variables Reference

### Required
- `GOOGLE_API_KEY` - Gemini API key from AI Studio

### Optional (Production)
- `GCP_PROJECT_ID` - Google Cloud project ID
- `GCP_LOCATION` - GCP region (default: us-central1)
- `BIGQUERY_DATASET` - BigQuery dataset name
- `GCS_BUCKET` - Cloud Storage bucket name
- `GOOGLE_APPLICATION_CREDENTIALS` - Path to GCP service account JSON

---

## 🚀 You're All Set!

Both backend and frontend dependencies are installed and ready to go. Follow the Quick Test section above to verify everything works, then use the `demo_script.md` for your hackathon presentation.

**Good luck! 🏆**

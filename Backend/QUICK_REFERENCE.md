# Aarogya AI - Backend Quick Reference

## 🚀 Quick Start (3 Steps)

### 1. Get API Key
```
Visit: https://console.groq.com
Sign up → API Keys → Create → Copy
```

### 2. Configure
```bash
# Edit Backend/.env
GOOGLE_API_KEY=gsk_your_key_here
```

### 3. Start
```bash
cd Backend
python -m uvicorn app.main:app --reload
```

---

## 📊 System Status

### Models
- **Primary**: llama-3.3-70b-versatile
- **Fallback**: llama-3.1-70b-versatile

### Rate Limits (Free Tier)
- 30 requests/minute
- 20,000 tokens/minute
- Unlimited daily

### Endpoints
- `POST /api/v1/hospital/optimize` - Hospital ops
- `POST /api/v1/diagnostic/diagnose` - Image analysis
- `POST /api/v1/mental-health/chat` - Mental health
- `POST /api/v1/treatment/recommend` - Treatment plans

---

## 🔧 Key Files

```
Backend/
├── app/
│   ├── config.py           # Central configuration
│   ├── utils/
│   │   └── groq_client.py  # API client wrapper
│   ├── agents/             # AI agents
│   ├── routes/             # API routes
│   └── main.py             # FastAPI app
└── .env                    # API key (YOU CREATE THIS)
```

---

## ⚙️ Configuration

### Agent Temperatures
```python
diagnostic: 0.2      # Precise medical analysis
treatment: 0.2       # Safe recommendations
mental_health: 0.7   # Empathetic responses
hospital: 0.3        # Balanced analysis
```

### Features
✅ Automatic retries (3x)
✅ Fallback model switching
✅ Rate limit handling
✅ Error categorization
✅ Usage tracking
✅ Startup validation

---

## 🧪 Testing

### Startup Check
```bash
python -c "from app.config import Config; Config.startup_check()"
```

### Full Test
```bash
python test_backend.py
```

### Manual Test
```bash
curl http://localhost:8000/health
```

---

## 🐛 Common Issues

### "API Key not configured"
→ Add key to `Backend/.env`

### "Invalid API Key"
→ Key must start with `gsk_`

### "Rate limit exceeded"
→ Wait 60 seconds (auto-handled)

### 404 errors
→ Check route registration in `main.py`

---

## 📈 Performance

### Response Times
- Hospital: ~2.1s
- Diagnostic: ~2.3s
- Mental Health: ~1.8s
- Treatment: ~2.0s

### Token Usage
- Hospital: ~1550 tokens
- Diagnostic: ~1300 tokens
- Mental Health: ~800 tokens
- Treatment: ~1800 tokens

---

## 🔒 Security Checklist

- [ ] API key in .env (not in code)
- [ ] .env in .gitignore
- [ ] Different keys for dev/prod
- [ ] Keys rotated monthly
- [ ] CORS properly configured

---

## 📞 Resources

- **Groq Console**: https://console.groq.com
- **Groq Docs**: https://console.groq.com/docs
- **API Status**: https://status.groq.com

---

## 💡 Pro Tips

1. **Cache responses** for repeated queries
2. **Monitor token usage** in Groq console
3. **Use fallback gracefully** - it's automatic
4. **Log errors** for debugging
5. **Test before demo** - run test_backend.py

---

**Need help? Check production_backend_guide.md**

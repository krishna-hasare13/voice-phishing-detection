# 🚀 Deployment Guide for VoiceShield

This guide explains how to deploy VoiceShield to production so users can access it from anywhere.

## ✅ What We Fixed for Deployment

### 1. **No More Temp Folder Issues**
- ✅ Changed from disk-based storage to **in-memory processing**
- ✅ Uses Python's `tempfile` module for temporary files
- ✅ Works on cloud platforms with read-only/ephemeral filesystems

### 2. **User-Friendly Interface**
- ✅ Created a **Control Panel** dashboard at `/control`
- ✅ Users just click "Start Detection" - no terminal needed
- ✅ Works entirely in the browser

---

## 🌐 Deployment Options

### Option 1: Render (Recommended - Free Tier Available)

**Why Render?**
- Free tier available
- Supports Python/FastAPI
- Easy deployment from GitHub
- Persistent storage with Supabase

**Steps:**

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/voice-phishing-detection.git
   git push -u origin main
   ```

2. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

3. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `voiceshield`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r backend/requirements.txt`
     - **Start Command**: `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`
     - **Instance Type**: Free

4. **Add Environment Variables**
   - `SUPABASE_URL`: Your Supabase URL
   - `SUPABASE_KEY`: Your Supabase API key

5. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment

6. **Access Your App**
   - URL: `https://voiceshield.onrender.com`
   - Control Panel: `https://voiceshield.onrender.com/control`

---

### Option 2: Railway

**Steps:**

1. **Push to GitHub** (same as above)

2. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

3. **Deploy**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Python and deploys

4. **Configure**
   - Add environment variables in Settings
   - Railway provides a public URL automatically

---

### Option 3: Heroku

**Steps:**

1. **Install Heroku CLI**
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create voiceshield
   ```

3. **Add Buildpack**
   ```bash
   heroku buildpacks:add heroku/python
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **Set Environment Variables**
   ```bash
   heroku config:set SUPABASE_URL=your_url
   heroku config:set SUPABASE_KEY=your_key
   ```

---

## 🔧 Pre-Deployment Checklist

### 1. Update `backend/app.py`
Make sure Supabase credentials are loaded from environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "your-default-url")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-default-key")
```

### 2. Create `.env` file (for local development)
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-api-key
```

### 3. Update `.gitignore`
```
.env
venv/
__pycache__/
*.pyc
.DS_Store
```

### 4. Test Locally
```bash
# Activate virtual environment
backend\venv\Scripts\activate

# Run server
uvicorn backend.app:app --reload

# Test at http://127.0.0.1:8000/control
```

---

## 📱 How Users Will Use It

### For Non-Technical Users:

1. **Visit the Website**
   - Go to `https://your-app-url.com`
   - They'll see the Control Panel automatically

2. **Click "Start Detection"**
   - Browser asks for microphone permission
   - Click "Allow"

3. **Make/Receive Calls**
   - The system listens and analyzes in real-time
   - Alerts appear if phishing is detected

4. **Click "Stop Detection"**
   - Stops monitoring
   - Can review transcripts

**No terminal, no Python, no technical knowledge needed!**

---

## 🔒 Security Notes

### For Production:

1. **Use Environment Variables**
   - Never commit API keys to GitHub
   - Use platform-specific env var management

2. **Enable HTTPS**
   - All platforms provide free SSL
   - Microphone access requires HTTPS

3. **Add CORS if needed**
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://your-frontend-domain.com"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

4. **Rate Limiting**
   - Consider adding rate limiting for API endpoints
   - Prevents abuse

---

## 🎯 Recommended Architecture

```
┌─────────────────┐
│   User Browser  │
│  (Control Panel)│
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Cloud Platform │
│  (Render/Railway)│
│                 │
│  ┌───────────┐  │
│  │  FastAPI  │  │
│  │  Backend  │  │
│  └─────┬─────┘  │
└────────┼────────┘
         │
         ↓
┌─────────────────┐
│    Supabase     │
│  (Database +    │
│   File Storage) │
└─────────────────┘
```

---

## 🐛 Troubleshooting

### Issue: "System Offline" in Control Panel
**Solution:** Backend isn't running. Check deployment logs.

### Issue: Microphone not working
**Solution:** 
- Ensure HTTPS is enabled
- Check browser permissions
- Try a different browser

### Issue: Slow processing
**Solution:**
- Upgrade to paid tier for more CPU
- Consider using GPU instances
- Optimize chunk size

---

## 📊 Monitoring

### Check Logs:
- **Render**: Dashboard → Logs tab
- **Railway**: Project → Deployments → Logs
- **Heroku**: `heroku logs --tail`

### Monitor Supabase:
- Database usage
- Storage usage
- API calls

---

## 🎉 You're Ready!

Your VoiceShield app is now:
- ✅ Deployment-ready (no temp folder issues)
- ✅ User-friendly (one-click start)
- ✅ Cloud-compatible (works on any platform)
- ✅ Secure (environment variables, HTTPS)

Deploy and protect users from voice phishing! 🛡️

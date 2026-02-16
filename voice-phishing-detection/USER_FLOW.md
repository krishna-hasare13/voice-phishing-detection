# 🎯 VoiceShield User Flow

## For Non-Technical Users (Control Panel)

```
┌─────────────────────────────────────────────────────────────┐
│                    USER JOURNEY                             │
└─────────────────────────────────────────────────────────────┘

Step 1: Visit Website
┌──────────────────────┐
│  Open Browser        │
│  Go to:              │
│  your-app.com        │
└──────────┬───────────┘
           │
           ↓
Step 2: See Control Panel
┌──────────────────────┐
│  ✨ VoiceShield      │
│  Control Panel       │
│                      │
│  [Start Detection]   │
│                      │
│  How it works:       │
│  • Mic activated     │
│  • Real-time AI      │
│  • Instant alerts    │
└──────────┬───────────┘
           │
           ↓
Step 3: Click "Start Detection"
┌──────────────────────┐
│  Browser asks:       │
│  "Allow microphone?" │
│                      │
│  [Block]  [Allow] ✓  │
└──────────┬───────────┘
           │
           ↓
Step 4: System Listening
┌──────────────────────┐
│  🎙️ Recording Active │
│                      │
│  Speak naturally.    │
│  System listening... │
│                      │
│  [Stop Detection]    │
└──────────┬───────────┘
           │
           ↓
Step 5: Real-Time Analysis
┌──────────────────────┐
│  Live Analysis       │
│  ─────────────────   │
│  ✅ "Hello, how      │
│     are you?"        │
│     Safe: 95%        │
│                      │
│  ⚠️  "Give me your   │
│     credit card"     │
│     Risk: 85%        │
└──────────┬───────────┘
           │
           ↓
Step 6: Phishing Alert (if detected)
┌──────────────────────┐
│  🚨 ALERT! 🚨        │
│                      │
│  PHISHING DETECTED   │
│      85%             │
│                      │
│  Terminate call      │
│  immediately!        │
└──────────┬───────────┘
           │
           ↓
Step 7: Stop Detection
┌──────────────────────┐
│  Click:              │
│  [Stop Detection]    │
│                      │
│  Review transcripts  │
│  and alerts          │
└──────────────────────┘

✅ DONE! No technical knowledge needed!
```

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    TECHNICAL FLOW                           │
└─────────────────────────────────────────────────────────────┘

User's Browser
┌────────────────────────┐
│  Control Panel         │
│  (control.html)        │
│                        │
│  JavaScript:           │
│  • MediaRecorder API   │
│  • WebSocket Client    │
│  • Audio Chunking      │
└───────┬────────────────┘
        │
        │ HTTPS + WebSocket
        │
        ↓
Cloud Platform (Render/Railway/Heroku)
┌────────────────────────┐
│  FastAPI Backend       │
│  (backend/app.py)      │
│                        │
│  Endpoints:            │
│  • /control            │
│  • /upload_chunk       │
│  • /ws/monitoring      │
│                        │
│  Processing:           │
│  • In-memory (no disk) │
│  • Whisper (tiny)      │
│  • DistilBERT          │
└───────┬────────────────┘
        │
        │ API Calls
        │
        ↓
Supabase
┌────────────────────────┐
│  Database              │
│  • chunks table        │
│  • call metadata       │
│                        │
│  Storage               │
│  • audio-chunks bucket │
│  • WAV files           │
└────────────────────────┘
```

---

## Deployment vs Local Development

### Local Development
```
Developer's Computer
├── Terminal 1: Backend Server
│   └── uvicorn backend.app:app --reload
│
├── Browser: Control Panel
│   └── http://127.0.0.1:8000/control
│
└── Optional: Terminal 2 for advanced features
    └── python main.py
```

### Production Deployment
```
Cloud Platform (Render)
├── Auto-starts backend on deploy
│   └── Runs: uvicorn backend.app:app
│
└── Public URL: https://your-app.onrender.com

Users
└── Just visit: https://your-app.onrender.com
    └── Control Panel loads automatically!
```

---

## Key Differences: Before vs After

### Before (Technical Users Only)
```
1. Install Python ❌
2. Create virtual environment ❌
3. Install dependencies ❌
4. Configure Supabase ❌
5. Open terminal ❌
6. Run: uvicorn backend.app:app ❌
7. Open another terminal ❌
8. Run: python main.py ❌
9. Type: start ❌
10. Use the system ✅
```

### After (Anyone Can Use)
```
1. Visit website ✅
2. Click "Start Detection" ✅
3. Allow microphone ✅
4. Use the system ✅
```

**10 steps → 4 steps!**
**Technical knowledge required → None!**

---

## Data Flow

```
User speaks
    ↓
Browser captures audio (MediaRecorder)
    ↓
Audio chunked every 10 seconds
    ↓
Chunk sent to backend via HTTP POST
    ↓
Backend processes in memory:
    1. Upload to Supabase Storage
    2. Transcribe with Whisper
    3. Classify with DistilBERT
    4. Calculate phishing score
    5. Store metadata in database
    ↓
Results sent back via WebSocket
    ↓
Browser displays:
    • Transcript
    • Risk level (Safe/Suspicious/Critical)
    • Alert if phishing detected
```

---

## Security Flow

```
Environment Variables (Deployment)
    ↓
SUPABASE_URL ────┐
SUPABASE_KEY ────┤
                 ↓
            Backend loads credentials
                 ↓
            Connects to Supabase
                 ↓
            Processes audio securely
                 ↓
            No credentials in code ✅
            No temp files on disk ✅
            HTTPS required ✅
```

---

## Comparison: Old vs New Storage

### Old (Disk-based)
```
Audio received
    ↓
Save to temp/chunk_123.wav ❌
    ↓
Process file
    ↓
Upload to Supabase
    ↓
Delete temp/chunk_123.wav

Problems:
• Fails on read-only filesystems
• Fails on ephemeral storage
• Slower (disk I/O)
• Cleanup issues
```

### New (In-memory)
```
Audio received
    ↓
Store in BytesIO (RAM) ✅
    ↓
Process from memory
    ↓
Upload to Supabase
    ↓
Auto-cleanup (garbage collection)

Benefits:
• Works on any platform
• Faster (no disk I/O)
• Automatic cleanup
• Cloud-ready
```

---

## User Experience Comparison

### Technical User (main.py)
```
Terminal Output:
🛡️  Voice Phishing Detection System
==================================================
Backend URL: http://127.0.0.1:8000
Chunk Duration: 5s
==================================================
🔧 Initializing system components...
🎙️  LinphoneCallRecorder initialized
📞 Starting call recording: call_20260216_134432
📊 Chunk 0 processed - Phishing: 4.24%
📊 Chunk 1 processed - Phishing: 35.08%
```

### Non-Technical User (Control Panel)
```
Browser Display:
┌─────────────────────────────┐
│ VoiceShield Control Panel   │
├─────────────────────────────┤
│ System Online ✅            │
│                             │
│ [Start Detection]           │
│                             │
│ Live Analysis:              │
│ ┌─────────────────────────┐ │
│ │ "Hello, how are you?"   │ │
│ │ Safe: 95%               │ │
│ └─────────────────────────┘ │
└─────────────────────────────┘
```

**Much more user-friendly!** 🎉

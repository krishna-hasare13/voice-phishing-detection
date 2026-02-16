# 🛡️ Voice Phishing Detection System

A simple, real-time system to detect phishing in phone calls using speech-to-text and AI.  
**Now with a user-friendly Control Panel - no technical knowledge required!**

## ✨ New Features

- 🎨 **Control Panel Dashboard** - One-click start/stop detection
- ☁️ **Deployment Ready** - Works on any cloud platform (Render, Railway, Heroku)
- 🚫 **No Temp Folders** - In-memory processing for cloud compatibility
- 🔒 **Secure** - Environment variable support for credentials

---

## 🚀 Quick Start (For Users)

### 1. **Clone the Project**

```sh
git clone <your-repo-url>
cd voice-phishing-detection
```

---

### 2. **Install Python Dependencies**

```sh
python -m venv venv
venv\Scripts\activate   # On Windows
# or
source venv/bin/activate   # On Linux/Mac

pip install -r requirements.txt
```

---

### 3. **Supabase Setup**

#### a. **Create a Supabase Project**
- Go to [https://app.supabase.com/](https://app.supabase.com/) and create a new project.

#### b. **Get Your Supabase URL and API Key**
- In your Supabase project, go to **Project Settings → API**.
- Copy the **Project URL** and **anon public API key**.

#### c. **Create a Table**
- Go to **Table Editor** in Supabase.
- Click **New Table** and name it `chunks`.
- Add these columns:
    | Name           | Type      |
    |----------------|-----------|
    | id             | bigint    | (Primary key, auto-increment)
    | call_id        | text      |
    | chunk_number   | int4      |
    | chunk_name     | text      |
    | file_url       | text      |
    | transcript     | text      |
    | phishing_score | float8    |
    | created_at     | timestamp | (default: now())

#### d. **Create a Storage Bucket**
- Go to **Storage** in Supabase.
- Create a bucket named `audio-chunks`.

---

### 4. **Configure Your Keys**

- Open `backend/app.py`.
- Find these lines at the top:
  ```python
  SUPABASE_URL = "Your-Supabase-URL"
  SUPABASE_KEY = "Your-Supabase-API-Key"
  ```
- Paste your Supabase URL and API key here.

---

### 5. **Download/Place the AI Model**

- Download or copy the `saved_model` folder (DistilBERT) into:  
  `classifier/saved_model/`
- If you use Whisper, make sure it downloads automatically or is available.

---

### 6. **Run the Backend**

```sh
backend\venv\Scripts\python -m uvicorn backend.app:app --reload
```
- The API runs at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

### 7. **Use the Control Panel** ⭐ NEW!

**For Non-Technical Users:**

1. Open your browser and go to: [http://127.0.0.1:8000/control](http://127.0.0.1:8000/control)
2. Click the **"Start Detection"** button
3. Allow microphone access when prompted
4. Speak or make calls - the system will analyze in real-time!
5. Click **"Stop Detection"** when done

**That's it! No terminal commands needed!**

**Alternative Dashboards:**
- **Upload Files**: [http://127.0.0.1:8000/upload](http://127.0.0.1:8000/upload)
- **Real-time Monitor**: [http://127.0.0.1:8000/realtime](http://127.0.0.1:8000/realtime)

---

### 8. **Run the Client (Advanced Users)**

- Edit `client/linphone_recorder.py` if you need to set the backend URL.
- Run:
  ```sh
  python client/linphone_recorder.py
  ```

---

### 8. **Use the Dashboard**

- Open the dashboard in your browser.
- Click **Start Monitoring** to see real-time transcripts and phishing alerts.

---

## 🛠️ Troubleshooting

- **Keys not working?** Double-check your Supabase URL and API key.
- **No data in dashboard?** Make sure your Supabase table and bucket names match exactly.
- **Model errors?** Ensure `classifier/saved_model/` exists and is not empty.

---

## 📋 Summary

- **Supabase**: Used for storing audio metadata and files.
- **Keys**: Set via environment variables or defaults in `backend/app.py`.
- **Table**: Name it `chunks` with the columns above.
- **Bucket**: Name it `audio-chunks`.
- **Control Panel**: [http://127.0.0.1:8000/control](http://127.0.0.1:8000/control)
- **Upload Page**: [http://127.0.0.1:8000/upload](http://127.0.0.1:8000/upload)
- **Real-time Monitor**: [http://127.0.0.1:8000/realtime](http://127.0.0.1:8000/realtime)

---

## ☁️ Deployment

**Ready to deploy to production?**

This project is now **deployment-ready** with:
- ✅ In-memory processing (no temp folder issues)
- ✅ Environment variable support
- ✅ User-friendly control panel
- ✅ Cloud platform compatibility

**See detailed deployment guides:**
- 📖 **[DEPLOYMENT.md](DEPLOYMENT.md)** - Step-by-step deployment instructions
- 📝 **[DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md)** - Overview of changes and features

**Recommended platforms:**
- [Render](https://render.com) (Free tier available)
- [Railway](https://railway.app)
- [Heroku](https://heroku.com)

---

**Need help?**  
Open an issue or ask in the project discussions!

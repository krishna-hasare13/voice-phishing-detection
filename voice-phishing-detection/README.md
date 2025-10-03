# Voice Phishing Detection 🚨

A real-time AI-powered **voice phishing (vishing) detection system** integrated with Linphone (VoIP softphone) to detect suspicious calls and protect users from fraud.  

This project leverages **OpenAI Whisper** for transcription and **BERT** for phishing classification.

---

## 🛠️ Features

- Real-time detection of voice phishing calls.
- Integration with Linphone to capture live call audio.
- Converts audio into text using Whisper.
- Classifies conversation segments as **phishing** or **normal** using BERT.
- Provides live alerts for suspicious calls.
- Modular architecture: client (Linphone), backend (FastAPI + AI), dashboard (optional).

---

## 📂 Repo Structure

voice-phishing-detection/
├── client/ # Linphone integration & audio chunking
├── backend/ # FastAPI + Whisper + BERT
├── dashboard/ # Web dashboard (optional)
├── data/ # Sample call recordings for testing
├── docs/ # Project docs & demo plan
├── tests/ # Unit & integration tests
├── README.md
└── LICENSE

python
Copy code


# -----------------------------
# Run Server
# -----------------------------
# Command to run: uvicorn app:app --reload
⚡ Installation & Setup
1. Clone the repo
bash
Copy code
git clone https://github.com/<your-username>/voice-phishing-detection.git
cd voice-phishing-detection/backend


2. Setup Python environment
bash
Copy code
python -m venv venv
# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux / Mac
source venv/bin/activate


3. Install dependencies
bash
Copy code
pip install fastapi uvicorn openai-whisper torch torchvision torchaudio transformers
🏃‍♂️ Run Backend Server
bash
Copy code
uvicorn app:app --reload
Server runs at: http://127.0.0.1:8000

Open Swagger docs to test endpoints: http://127.0.0.1:8000/docs

🧪 Testing API
Using Swagger Docs
Go to http://127.0.0.1:8000/docs

Find /predict endpoint.

Click Try it out, upload a .wav file, and click Execute.

Response example:

json
Copy code
{
  "transcription": "Hello, we are calling from your bank...",
  "prediction": {
    "normal": 0.12,
    "phishing": 0.88
  }
}
Using Python Script
python
Copy code
import requests

url = "http://127.0.0.1:8000/predict"
files = {"file": open("sample_audio.wav", "rb")}

response = requests.post(url, files=files)
print(response.json())
🏗️ How It Works
Client (Linphone) records call audio in 10-second chunks.

Backend transcribes audio using Whisper.

BERT model predicts whether the conversation is phishing or normal.

Dashboard (optional) displays live alerts.

📈 Future Improvements
Full real-time RTP audio streaming integration with Linphone SDK.

Enhanced BERT model trained on larger vishing dataset.

Mobile-friendly dashboard for instant alerts.

Integration with notifications for end-users.
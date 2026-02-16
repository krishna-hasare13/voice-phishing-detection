
import requests
import os

url = "http://127.0.0.1:8000/upload_chunk/"
file_path = r"d:\coding\voice-phishing-detection\phish.wav"
call_id = "test_manual_upload"
chunk_number = 1

if os.path.exists(file_path):
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f, "audio/wav")}
        data = {"call_id": call_id, "chunk_number": chunk_number}
        print(f"Sending {file_path} to {url}...")
        try:
            response = requests.post(url, files=files, data=data, timeout=60)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
        except Exception as e:
            print(f"Error: {e}")
else:
    print(f"File not found: {file_path}")

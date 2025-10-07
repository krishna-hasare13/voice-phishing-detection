# Voice Phishing Detection System - Linphone Integration

This system provides real-time voice phishing detection integrated with Linphone desktop application for call recording and analysis.

## 🎯 Features

- **Real-time Call Recording**: Captures audio from Linphone calls automatically
- **Live Phishing Detection**: Analyzes speech in 10-second chunks using AI models
- **Web Dashboard**: Real-time monitoring with WebSocket-based alerts
- **Automatic Transcription**: Uses OpenAI Whisper for speech-to-text
- **Machine Learning**: DistilBERT model for phishing classification
- **Alert System**: Instant notifications for suspicious calls

## 🛠️ Prerequisites

### System Requirements
- Windows 10/11
- Python 3.8+
- Linphone Desktop Application
- Microphone access

### Software Installation

1. **Install Linphone Desktop**
   - Download from: https://www.linphone.org/
   - Install and configure with your SIP account
   - Ensure microphone permissions are granted

2. **Install Python Dependencies**
   ```powershell
   # Navigate to project directory
   cd C:\Users\K\Desktop\voice-phishing-detection\voice-phishing-detection

   # Install backend dependencies
   cd backend
   pip install -r requirements.txt

   # For PyAudio on Windows, you might need:
   pip install pipwin
   pipwin install pyaudio
   ```

3. **Verify Audio System**
   ```powershell
   python -c "import pyaudio; print('PyAudio OK')"
   python -c "import whisper; print('Whisper OK')"
   ```

## 🚀 Quick Start

### Method 1: Interactive Mode (Recommended)

1. **Start the Backend Server**
   ```powershell
   cd backend
   uvicorn app:app --reload --host 127.0.0.1 --port 8000
   ```

2. **Start the Main System**
   ```powershell
   # In a new terminal
   cd C:\Users\K\Desktop\voice-phishing-detection\voice-phishing-detection
   python main.py
   ```

3. **Open Web Dashboard**
   - Open browser: http://127.0.0.1:8000/static/realtime.html
   - You'll see the real-time monitoring interface

4. **Start Monitoring**
   In the main system terminal:
   ```
   📞 VPD> start
   ✅ Monitoring started for call: call_20251006_143052_a1b2c3d4
   ```

5. **Make/Receive Calls in Linphone**
   - System will automatically detect audio
   - Transcription and analysis happen in real-time
   - Alerts appear on dashboard and console

### Method 2: Automatic Mode

```powershell
# Auto-start monitoring for 60 seconds
python main.py --auto --duration 60

# Auto-start monitoring indefinitely
python main.py --auto
```

## 🎮 Interactive Commands

When running in interactive mode:

- `start [call_id]` - Start monitoring (optional custom call_id)
- `stop` - Stop current monitoring
- `status` - Show system status
- `help` - Show available commands
- `quit` - Exit system

## 🌐 Web Dashboard Features

Access the dashboard at: http://127.0.0.1:8000/static/realtime.html

- **Live Call Status**: Shows active call information
- **Real-time Transcripts**: Speech-to-text results as they happen
- **Phishing Alerts**: Immediate warnings for suspicious content
- **Statistics**: Call counts, alerts, chunks processed
- **WebSocket Connection**: Real-time updates without page refresh

## 🔧 Configuration Options

### Backend URL
```powershell
python main.py --backend http://localhost:8001
```

### Chunk Duration
```powershell
python main.py --chunk-duration 5  # 5-second chunks instead of 10
```

### Custom Call ID
```powershell
python main.py --auto --call-id "my_test_call_001"
```

## 📊 How It Works

1. **Audio Capture**: System captures microphone audio in real-time
2. **Chunking**: Audio is processed in configurable chunks (default: 10 seconds)
3. **Transcription**: Each chunk is transcribed using Whisper
4. **Classification**: DistilBERT model analyzes text for phishing indicators
5. **Alerting**: High-confidence phishing attempts trigger immediate alerts
6. **Storage**: Results are stored in Supabase database
7. **Real-time Updates**: WebSocket pushes updates to dashboard

## 🚨 Alert Thresholds

- **Medium Alert**: Phishing confidence > 60%
- **High Alert**: Phishing confidence > 80%
- **Real-time Notifications**: Browser notifications for alerts
- **Visual Indicators**: Color-coded confidence scores

## 🔍 Troubleshooting

### Common Issues

1. **PyAudio Installation Error**
   ```powershell
   pip install pipwin
   pipwin install pyaudio
   ```

2. **Microphone Not Detected**
   - Check Windows microphone permissions
   - Verify Linphone can access microphone
   - Test with: `python -c "import pyaudio; p=pyaudio.PyAudio(); print(p.get_device_count())"`

3. **WebSocket Connection Failed**
   - Ensure backend is running on port 8000
   - Check firewall settings
   - Verify URL: ws://127.0.0.1:8000/ws/call_monitoring/

4. **Whisper Model Loading Error**
   - First run downloads models automatically
   - Ensure stable internet connection
   - Clear cache: Delete `~/.cache/whisper/`

5. **Backend Connection Error**
   - Verify backend server is running: http://127.0.0.1:8000
   - Check network connectivity
   - Review backend logs for errors

### Debug Mode

Enable verbose logging:
```powershell
python main.py --backend http://127.0.0.1:8000 --auto --duration 30
```

## 📁 Project Structure

```
voice-phishing-detection/
├── main.py                      # Main integration script
├── backend/
│   ├── app.py                   # Enhanced FastAPI backend
│   └── requirements.txt         # Backend dependencies
├── client/
│   ├── linphone_recorder.py     # Linphone integration module
│   └── send_to_backend.py       # Original client
├── dashboard/
│   └── web/
│       ├── index.html           # Original dashboard
│       └── realtime.html        # New real-time dashboard
└── classifier/
    └── saved_model/             # Pre-trained models
```

## 🔄 Workflow Example

1. Start backend: `uvicorn app:app --reload`
2. Start main system: `python main.py`
3. Open dashboard: http://127.0.0.1:8000/static/realtime.html
4. Start monitoring: `start my_call_001`
5. Make call in Linphone
6. Watch real-time transcription and alerts
7. Stop monitoring: `stop`

## 📱 Integration with Linphone

The system captures audio from your system's default microphone, which should be the same microphone Linphone uses for calls. This approach works with:

- **Incoming Calls**: System detects and analyzes incoming call audio
- **Outgoing Calls**: System analyzes your outgoing calls
- **Conference Calls**: Works with multi-party calls
- **VoIP Protocols**: Compatible with SIP, RTP, and other VoIP protocols

## 🔒 Security Considerations

- Audio data is processed locally and in real-time
- Temporary audio files are automatically cleaned up
- WebSocket connections are local (127.0.0.1)
- Supabase credentials should be secured in production
- Consider using HTTPS/WSS for production deployments

## 🎯 Performance Optimization

- **Chunk Size**: Smaller chunks = faster response, higher CPU usage
- **Model Selection**: Whisper "base" model balances speed/accuracy
- **Memory Usage**: System manages audio buffers automatically
- **CPU Usage**: Monitor system resources during long calls

## 📈 Future Enhancements

- Integration with VoIP APIs (Twilio, etc.)
- Multiple language support
- Advanced phishing pattern detection
- Call recording file export
- Integration with security systems
- Mobile app companion

## 🆘 Support

For issues or questions:
1. Check troubleshooting section above
2. Verify all prerequisites are installed
3. Test with demo mode: `python main.py --auto --duration 30`
4. Review backend logs and console output

---

**🛡️ Stay Protected! The system helps detect voice phishing attempts in real-time.**
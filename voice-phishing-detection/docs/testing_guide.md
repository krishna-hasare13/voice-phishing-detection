# 📞 Complete Linphone Testing Guide

## 🎯 Quick Setup for Testing

### Step 1: Prepare the System
```powershell
# Terminal 1: Start Backend
cd backend
uvicorn app:app --reload

# Terminal 2: Open for testing
cd ..
# (Keep this ready for running tests)
```

### Step 2: Open Dashboard
- Browser: http://127.0.0.1:8000/realtime
- This shows real-time monitoring

### Step 3: Choose Your Test Method

## 🧪 Method A: Echo Test (No Linphone Setup Required)
```powershell
# Run the test simulator
python linphone_test.py

# Select option 2 for phishing test or 1 for normal conversation
```

## 📞 Method B: Real Linphone Call Test

### B1: Setup Free SIP Account
1. **Get Free SIP Account:**
   - Visit: https://www.antisip.com/
   - Sign up for free account
   - Note: Username, Password, Domain

2. **Configure Linphone:**
   - Open Linphone Desktop
   - Settings → Accounts → Add Account
   - Enter your credentials
   - Test registration (should show green checkmark)

### B2: Test with Echo Service
1. **Start Monitoring:**
   ```powershell
   python main.py
   📞 VPD> start linphone_echo_call
   ```

2. **In Linphone, call one of these echo services:**
   - `sip:echo@conference.sip2sip.info`
   - `sip:17747@sip2sip.info`
   - `sip:music@iptel.org` (plays music)

3. **Speak Test Phrases:**
   - Normal: "Hello, this is a test call"
   - Phishing: "Give me your credit card number immediately"
   - Watch dashboard for alerts!

### B3: Test with Another Person
1. **Both people need:**
   - Linphone installed
   - Same SIP provider accounts
   - Or one person calls the other's SIP address

2. **Test Scenarios:**
   - Normal conversation
   - One person acts as "scammer" (for testing)
   - Watch real-time detection

## 🎬 Method C: Automated Test Scenarios

### C1: Phishing Detection Test
```powershell
python linphone_test.py
# Choose option 2 - Phishing Test
# Follow the script and speak the suggested phrases
# Expected: HIGH ALERT warnings
```

### C2: Normal Call Test  
```powershell
python linphone_test.py
# Choose option 1 - Normal Call
# Speak business-like phrases
# Expected: LOW phishing scores
```

## 📊 What to Watch For

### ✅ Normal Behavior:
- WebSocket connection established
- Audio chunks processed every 10 seconds
- Transcription appears in real-time
- Low phishing scores (0-30%)
- Green indicators on dashboard

### 🚨 Phishing Detection:
- High phishing scores (60%+)
- Red alert notifications
- Browser notifications (if enabled)
- Alert sounds/visual warnings
- Detailed transcript of suspicious content

## 🔧 Troubleshooting Common Issues

### Issue: No Audio Detected
```powershell
# Check microphone
python -c "import pyaudio; p=pyaudio.PyAudio(); print(f'Devices: {p.get_device_count()}')"

# Test microphone permissions
# Windows Settings → Privacy → Microphone → Allow apps
```

### Issue: Linphone Not Connecting
- Check SIP credentials
- Try different SIP providers
- Ensure internet connection
- Check firewall settings

### Issue: WebSocket Connection Failed
- Ensure backend is running on port 8000
- Check: http://127.0.0.1:8000
- Try restarting backend server

### Issue: No Transcription
- Check Whisper model download
- Ensure microphone input levels
- Try speaking louder/clearer

## 🎯 Test Validation Checklist

✅ **Audio Capture Test:**
- [ ] Microphone detected and working
- [ ] Audio chunks being processed (see console output)
- [ ] No "audio device" errors

✅ **Transcription Test:**
- [ ] Speech converted to text accurately
- [ ] Text appears in dashboard "Live Transcripts"
- [ ] Transcription happens within 10-15 seconds

✅ **WebSocket Test:**
- [ ] Dashboard shows "Connected" status
- [ ] Real-time updates without page refresh
- [ ] Live call status updates

✅ **Phishing Detection Test:**
- [ ] Normal speech shows low scores (0-30%)
- [ ] Suspicious phrases trigger alerts (60%+)
- [ ] Alerts appear in dashboard immediately
- [ ] Browser notifications work

✅ **End-to-End Test:**
- [ ] Start monitoring → Make call → See transcription → Get alerts → Stop monitoring
- [ ] All data saves to database
- [ ] Clean shutdown without errors

## 🚀 Production Usage Tips

1. **For Real Linphone Integration:**
   - Install Linphone Desktop
   - Configure with your VoIP provider
   - Start monitoring before making/receiving calls
   - Keep dashboard open for real-time alerts

2. **For Business Use:**
   - Set up dedicated monitoring station
   - Configure alert thresholds
   - Train staff on recognizing alerts
   - Log all suspicious calls for review

3. **For Personal Protection:**
   - Run system during important calls
   - Monitor elderly family members' calls
   - Use with telemarketing/unknown numbers
   - Keep system updated with latest models

---

**🛡️ Remember: This system helps detect potential phishing, but human judgment is still important for final decisions!**
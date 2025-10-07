"""
Real-time Linphone Call Recorder for Voice Phishing Detection
Captures audio from Linphone calls and sends chunks for analysis
"""

import time
import threading
import wave
import numpy as np
import requests
import json
from queue import Queue
import pyaudio
import os
import uuid
from datetime import datetime

try:
    import websocket
except ImportError:
    print("⚠️  WebSocket library not found. Installing...")
    import subprocess
    subprocess.check_call(["pip", "install", "websocket-client"])
    import websocket

class LinphoneCallRecorder:
    def __init__(self, 
                 backend_url="http://127.0.0.1:8000",
                 chunk_duration=10,  # seconds
                 sample_rate=16000,
                 channels=1):
        
        self.backend_url = backend_url
        self.chunk_duration = chunk_duration
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = sample_rate * chunk_duration
        
        # Recording state
        self.is_recording = False
        self.current_call_id = None
        self.chunk_number = 0
        self.audio_buffer = []
        
        # WebSocket for real-time updates
        self.ws = None
        self.ws_connected = False
        
        # Audio capture
        self.audio = pyaudio.PyAudio()
        self.stream = None
        
        # Threading
        self.recording_thread = None
        self.processing_thread = None
        self.audio_queue = Queue()
        
        print("🎙️  LinphoneCallRecorder initialized")
        print(f"   Backend: {self.backend_url}")
        print(f"   Chunk duration: {self.chunk_duration}s")
        print(f"   Sample rate: {self.sample_rate}Hz")
    
    def start_call_recording(self, call_id=None):
        """Start recording a new call"""
        if self.is_recording:
            print("⚠️  Already recording a call. Stop current call first.")
            return False
        
        # Generate call ID if not provided
        if not call_id:
            call_id = f"call_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        
        self.current_call_id = call_id
        self.chunk_number = 0
        self.audio_buffer = []
        self.is_recording = True
        
        print(f"📞 Starting call recording: {call_id}")
        
        # Initialize call monitoring on backend
        self._initialize_call_monitoring()
        
        # Start WebSocket connection
        self._connect_websocket()
        
        # Start audio capture
        self._start_audio_capture()
        
        # Start processing thread
        self.processing_thread = threading.Thread(target=self._process_audio_chunks)
        self.processing_thread.daemon = True
        self.processing_thread.start()
        
        print("✅ Call recording started successfully")
        return True
    
    def stop_call_recording(self):
        """Stop the current call recording"""
        if not self.is_recording:
            print("⚠️  No active recording to stop")
            return
        
        print(f"🛑 Stopping call recording: {self.current_call_id}")
        
        self.is_recording = False
        
        # Stop audio capture
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        
        # Process any remaining audio in buffer
        if len(self.audio_buffer) > 0:
            self._process_final_chunk()
        
        # Close WebSocket
        if self.ws:
            self.ws.close()
            self.ws = None
            self.ws_connected = False
        
        # Finalize call on backend
        self._finalize_call()
        
        print("✅ Call recording stopped")
    
    def _initialize_call_monitoring(self):
        """Initialize call monitoring on the backend"""
        try:
            response = requests.post(
                f"{self.backend_url}/start_call_monitoring/",
                data={"call_id": self.current_call_id}
            )
            if response.status_code == 200:
                print("✅ Backend call monitoring initialized")
            else:
                print(f"⚠️  Failed to initialize backend monitoring: {response.status_code}")
        except Exception as e:
            print(f"❌ Error initializing backend: {e}")
    
    def _connect_websocket(self):
        """Connect to backend WebSocket for real-time updates"""
        try:
            ws_url = f"ws://127.0.0.1:8000/ws/call_monitoring/{self.current_call_id}"
            
            def on_message(ws, message):
                try:
                    data = json.loads(message)
                    self._handle_websocket_message(data)
                except Exception as e:
                    print(f"❌ WebSocket message error: {e}")
            
            def on_error(ws, error):
                print(f"❌ WebSocket error: {error}")
                self.ws_connected = False
            
            def on_close(ws, close_status_code, close_msg):
                print("🔌 WebSocket connection closed")
                self.ws_connected = False
            
            def on_open(ws):
                print("🔌 WebSocket connected")
                self.ws_connected = True
            
            self.ws = websocket.WebSocketApp(
                ws_url,
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )
            
            # Start WebSocket in separate thread
            ws_thread = threading.Thread(target=self.ws.run_forever)
            ws_thread.daemon = True
            ws_thread.start()
            
        except Exception as e:
            print(f"❌ WebSocket connection failed: {e}")
    
    def _start_audio_capture(self):
        """Start capturing audio from microphone"""
        try:
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=1024,
                stream_callback=self._audio_callback
            )
            self.stream.start_stream()
            print("🎤 Audio capture started")
        except Exception as e:
            print(f"❌ Failed to start audio capture: {e}")
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Callback for audio data"""
        if self.is_recording:
            # Convert bytes to numpy array
            audio_data = np.frombuffer(in_data, dtype=np.int16)
            self.audio_queue.put(audio_data)
        
        return (in_data, pyaudio.paContinue)
    
    def _process_audio_chunks(self):
        """Process audio chunks in separate thread"""
        while self.is_recording:
            try:
                # Get audio data from queue
                if not self.audio_queue.empty():
                    audio_data = self.audio_queue.get()
                    
                    # Convert to list and extend buffer
                    if isinstance(audio_data, np.ndarray):
                        self.audio_buffer.extend(audio_data.tolist())
                    else:
                        self.audio_buffer.extend(audio_data)
                    
                    # Check if we have enough data for a chunk
                    if len(self.audio_buffer) >= self.chunk_size:
                        chunk_data = self.audio_buffer[:self.chunk_size]
                        self.audio_buffer = self.audio_buffer[self.chunk_size:]
                        
                        # Process this chunk (convert back to numpy array)
                        chunk_array = np.array(chunk_data, dtype=np.int16)
                        self._send_chunk_to_backend(chunk_array)
                        self.chunk_number += 1
                
                time.sleep(0.1)  # Small delay to prevent busy waiting
                
            except Exception as e:
                print(f"❌ Error processing audio chunk: {e}")
    
    def _send_chunk_to_backend(self, audio_data):
        """Send audio chunk to backend for processing"""
        try:
            # Ensure audio_data is a numpy array
            if isinstance(audio_data, list):
                audio_data = np.array(audio_data, dtype=np.int16)
            elif not isinstance(audio_data, np.ndarray):
                audio_data = np.array(audio_data, dtype=np.int16)
            
            # Convert numpy array to WAV bytes
            wav_data = self._convert_to_wav(audio_data)
            
            # Send to backend
            files = {'file': (f'chunk_{self.chunk_number}.wav', wav_data, 'audio/wav')}
            data = {
                'call_id': self.current_call_id,
                'chunk_number': self.chunk_number
            }
            
            response = requests.post(
                f"{self.backend_url}/upload_realtime_chunk/",
                files=files,
                data=data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                self._handle_analysis_result(result)
                print(f"📊 Chunk {self.chunk_number} processed - Phishing: {result['prediction']['phishing']:.2%}")
            else:
                print(f"⚠️  Backend processing failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error sending chunk to backend: {e}")
    
    def _convert_to_wav(self, audio_data):
        """Convert numpy audio data to WAV bytes"""
        import io
        
        # Create WAV file in memory
        wav_io = io.BytesIO()
        
        with wave.open(wav_io, 'wb') as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(audio_data.astype(np.int16).tobytes())
        
        wav_io.seek(0)
        return wav_io.read()
    
    def _handle_analysis_result(self, result):
        """Handle analysis result from backend"""
        phishing_score = result.get('prediction', {}).get('phishing', 0)
        transcript = result.get('transcript', '')
        
        # Show high-confidence phishing alerts
        if phishing_score > 0.6:
            self._show_phishing_alert(result)
        
        # Send real-time update via WebSocket if connected
        if self.ws_connected and self.ws:
            update = {
                "type": "analysis_update",
                "call_id": self.current_call_id,
                "chunk_number": self.chunk_number,
                "transcript": transcript,
                "phishing_score": phishing_score,
                "timestamp": time.time()
            }
            try:
                self.ws.send(json.dumps(update))
            except Exception as e:
                print(f"❌ Error sending WebSocket update: {e}")
    
    def _show_phishing_alert(self, result):
        """Show phishing alert"""
        phishing_score = result['prediction']['phishing']
        transcript = result.get('transcript', '')
        
        print(f"\n🚨 {'='*50}")
        print(f"🚨 PHISHING ALERT - Call: {self.current_call_id}")
        print(f"🚨 Confidence: {phishing_score:.1%}")
        print(f"🚨 Transcript: {transcript}")
        print(f"🚨 Time: {datetime.now().strftime('%H:%M:%S')}")
        print(f"🚨 {'='*50}\n")
        
        # You could add additional alert mechanisms here:
        # - Windows toast notifications
        # - Email alerts
        # - Sound alerts
        # - Log to file
    
    def _process_final_chunk(self):
        """Process any remaining audio data"""
        if len(self.audio_buffer) > 0:
            print(f"📊 Processing final chunk with {len(self.audio_buffer)} samples")
            chunk_array = np.array(self.audio_buffer, dtype=np.int16)
            self._send_chunk_to_backend(chunk_array)
    
    def _finalize_call(self):
        """Finalize call on backend"""
        try:
            response = requests.post(
                f"{self.backend_url}/finalize_call/",
                data={"call_id": self.current_call_id}
            )
            if response.status_code == 200:
                print("✅ Call finalized on backend")
            else:
                print(f"⚠️  Failed to finalize call: {response.status_code}")
        except Exception as e:
            print(f"❌ Error finalizing call: {e}")
    
    def _handle_websocket_message(self, data):
        """Handle incoming WebSocket messages"""
        msg_type = data.get('type')
        
        if msg_type == 'phishing_alert':
            print(f"🔔 Real-time alert received: {data}")
        elif msg_type == 'system_message':
            print(f"💬 System: {data.get('message', '')}")
        else:
            print(f"📨 WebSocket message: {data}")
    
    def get_status(self):
        """Get current recording status"""
        return {
            "is_recording": self.is_recording,
            "call_id": self.current_call_id,
            "chunk_number": self.chunk_number,
            "ws_connected": self.ws_connected,
            "buffer_size": len(self.audio_buffer)
        }
    
    def cleanup(self):
        """Cleanup resources"""
        if self.is_recording:
            self.stop_call_recording()
        
        if self.audio:
            self.audio.terminate()
        
        print("🧹 Resources cleaned up")

# Test/Demo function
def demo_recording(duration_seconds=30):
    """Demo function to test recording for a specified duration"""
    recorder = LinphoneCallRecorder()
    
    try:
        print(f"🎬 Starting demo recording for {duration_seconds} seconds...")
        
        # Start recording
        if recorder.start_call_recording("demo_call_001"):
            
            # Record for specified duration
            time.sleep(duration_seconds)
            
            # Stop recording
            recorder.stop_call_recording()
            
        print("🎬 Demo recording completed")
        
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
        recorder.stop_call_recording()
    
    finally:
        recorder.cleanup()

if __name__ == "__main__":
    # Run demo if called directly
    demo_recording(20)  # 20 second demo
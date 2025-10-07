#!/usr/bin/env python3
"""
Quick Test Script for Voice Phishing Detection System
Tests the system with a short demo recording
"""

import subprocess
import sys
import time
import requests

def test_backend_connection():
    """Test if backend is running"""
    try:
        response = requests.get("http://127.0.0.1:8000/")
        print("✅ Backend is running")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running. Please start it with:")
        print("   cd backend && uvicorn app:app --reload")
        return False

def run_system_test():
    """Run a quick system test"""
    print("🧪 Running Voice Phishing Detection System Test")
    print("=" * 50)
    
    # Check backend
    if not test_backend_connection():
        return False
    
    # Run demo
    print("🎬 Starting 15-second demo recording...")
    print("💬 Speak something to test the system!")
    print("   Try saying: 'Hello, this is a test call'")
    print("   Or: 'Give me your credit card information' (phishing test)")
    
    try:
        # Run the main system in auto mode for 15 seconds
        result = subprocess.run([
            sys.executable, "main.py", 
            "--auto", "--duration", "15"
        ], capture_output=True, text=True, timeout=30)
        
        print("\n" + "="*50)
        print("📊 Test Results:")
        print("="*50)
        print(result.stdout)
        
        if result.stderr:
            print("⚠️  Errors/Warnings:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ System test completed successfully!")
            return True
        else:
            print("❌ System test failed")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Test timed out")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def main():
    """Main test function"""
    print("🛡️  Voice Phishing Detection System - Quick Test")
    print("This will test the system with a 15-second recording")
    print()
    
    input("Press Enter to start the test (make sure your microphone is working)...")
    
    success = run_system_test()
    
    if success:
        print("\n🎉 Test completed! The system is working correctly.")
        print("\n🌐 Next steps:")
        print("1. Open the dashboard: http://127.0.0.1:8000/realtime")
        print("2. Run interactive mode: python main.py")
        print("3. Make calls with Linphone and monitor in real-time!")
    else:
        print("\n💥 Test failed. Please check the error messages above.")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure backend is running: cd backend && uvicorn app:app --reload")
        print("2. Install dependencies: pip install -r backend/requirements.txt")
        print("3. Check microphone permissions")

if __name__ == "__main__":
    main()
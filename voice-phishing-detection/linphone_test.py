#!/usr/bin/env python3
"""
Linphone Call Test Simulator
Simulates different call scenarios for testing the voice phishing detection system
"""

import time
import threading
import sys
import os

def run_test_scenario(scenario_name, duration=30):
    """Run a specific test scenario"""
    
    scenarios = {
        "normal_call": {
            "description": "Normal business conversation",
            "instructions": [
                "Say: 'Hello, this is John from ABC Company'",
                "Say: 'I'm calling about your recent inquiry'", 
                "Say: 'Would you like to schedule a meeting?'",
                "Say: 'Thank you for your time'"
            ]
        },
        "phishing_test": {
            "description": "Phishing attempt simulation (for testing only)",
            "instructions": [
                "Say: 'This is urgent! Your bank account has been compromised'",
                "Say: 'I need to verify your account information immediately'",
                "Say: 'Please provide your credit card number for verification'",
                "Say: 'Act quickly or your account will be closed'"
            ]
        },
        "tech_support_scam": {
            "description": "Tech support scam simulation",
            "instructions": [
                "Say: 'This is Microsoft technical support'",
                "Say: 'We detected viruses on your computer'",
                "Say: 'Please install this remote access software'",
                "Say: 'We need your Windows license key to fix it'"
            ]
        },
        "interactive_test": {
            "description": "Interactive testing - speak naturally",
            "instructions": [
                "Speak naturally into your microphone",
                "Try different types of conversations",
                "Test both normal and suspicious phrases",
                "Watch the dashboard for real-time analysis"
            ]
        }
    }
    
    if scenario_name not in scenarios:
        print(f"❌ Unknown scenario: {scenario_name}")
        print(f"Available scenarios: {', '.join(scenarios.keys())}")
        return
    
    scenario = scenarios[scenario_name]
    
    print(f"🎬 Test Scenario: {scenario['description']}")
    print("=" * 60)
    print(f"⏱️  Duration: {duration} seconds")
    print()
    print("📋 Test Instructions:")
    for i, instruction in enumerate(scenario['instructions'], 1):
        print(f"   {i}. {instruction}")
    print()
    print("🎤 Speak clearly into your microphone")
    print("🌐 Watch the dashboard at: http://127.0.0.1:8000/realtime")
    print("=" * 60)
    
    input("Press Enter when ready to start the test...")
    
    # Import and run the main system
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, "main.py",
            "--auto", "--duration", str(duration),
            "--call-id", f"test_{scenario_name}_{int(time.time())}"
        ], cwd=os.path.dirname(__file__))
        
        print("\n✅ Test completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

def main():
    """Main test menu"""
    print("🛡️  Linphone Call Test Simulator")
    print("=" * 50)
    print()
    print("📞 Test Scenarios:")
    print("1. normal_call     - Normal business conversation")
    print("2. phishing_test   - Phishing attempt (HIGH ALERT expected)")
    print("3. tech_support_scam - Tech support scam (HIGH ALERT expected)")
    print("4. interactive_test - Free-form testing")
    print()
    print("🔧 Prerequisites:")
    print("- Backend running: uvicorn app:app --reload (in backend/ folder)")
    print("- Dashboard open: http://127.0.0.1:8000/realtime")
    print("- Microphone working and permissions granted")
    print()
    
    while True:
        try:
            choice = input("Select test scenario (1-4) or 'q' to quit: ").strip().lower()
            
            if choice == 'q':
                break
            
            scenarios = {
                '1': 'normal_call',
                '2': 'phishing_test', 
                '3': 'tech_support_scam',
                '4': 'interactive_test'
            }
            
            if choice in scenarios:
                duration = input("Test duration in seconds (default: 30): ").strip()
                duration = int(duration) if duration.isdigit() else 30
                
                run_test_scenario(scenarios[choice], duration)
                
                if input("\nRun another test? (y/n): ").strip().lower() != 'y':
                    break
            else:
                print("❌ Invalid choice. Please select 1-4 or 'q'")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
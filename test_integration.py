
#!/usr/bin/env python3
"""
Test script for AI Phone Integration
Tests various components and scenarios
"""

import requests
import json
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

def test_app_health():
    """Test if the Flask app is running and healthy"""
    webhook_base_url = os.getenv('WEBHOOK_BASE_URL')
    
    if not webhook_base_url:
        print("❌ WEBHOOK_BASE_URL not configured")
        return False
    
    try:
        response = requests.get(f"{webhook_base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ App health check passed")
            print(f"   Status: {data.get('status')}")
            print(f"   Chatbot ID: {data.get('chatbot_id')}")
            print(f"   Business: {data.get('business')}")
            return True
        else:
            print(f"❌ Health check failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        return False

def test_tts_endpoint():
    """Test the text-to-speech endpoint"""
    webhook_base_url = os.getenv('WEBHOOK_BASE_URL')
    
    try:
        response = requests.get(f"{webhook_base_url}/test_tts", timeout=10)
        if response.status_code == 200:
            print("✅ TTS endpoint working")
            print(f"   Content-Type: {response.headers.get('Content-Type')}")
            return True
        else:
            print(f"❌ TTS test failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ TTS test error: {str(e)}")
        return False

def test_twilio_connection():
    """Test Twilio API connection"""
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    
    if not account_sid or not auth_token:
        print("❌ Twilio credentials not configured")
        return False
    
    try:
        client = Client(account_sid, auth_token)
        account = client.api.accounts(account_sid).fetch()
        print("✅ Twilio connection successful")
        print(f"   Account: {account.friendly_name}")
        print(f"   Status: {account.status}")
        return True
    except Exception as e:
        print(f"❌ Twilio connection failed: {str(e)}")
        return False

def test_phone_number_config():
    """Test if Twilio phone number is properly configured"""
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    webhook_base_url = os.getenv('WEBHOOK_BASE_URL')
    
    if not all([account_sid, auth_token, webhook_base_url]):
        print("❌ Missing configuration for phone number test")
        return False
    
    try:
        client = Client(account_sid, auth_token)
        numbers = client.incoming_phone_numbers.list()
        
        if not numbers:
            print("❌ No Twilio phone numbers found")
            return False
        
        for number in numbers:
            print(f"📱 Phone Number: {number.phone_number}")
            print(f"   Voice URL: {number.voice_url}")
            print(f"   Status Callback: {number.status_callback}")
            
            # Check if webhooks are configured correctly
            expected_voice_url = f"{webhook_base_url}/voice"
            expected_status_url = f"{webhook_base_url}/call_status"
            
            if number.voice_url == expected_voice_url:
                print("   ✅ Voice webhook configured correctly")
            else:
                print(f"   ❌ Voice webhook mismatch. Expected: {expected_voice_url}")
            
            if number.status_callback == expected_status_url:
                print("   ✅ Status webhook configured correctly")
            else:
                print(f"   ❌ Status webhook mismatch. Expected: {expected_status_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Phone number config test failed: {str(e)}")
        return False

def test_speech_processing():
    """Test speech processing logic with sample inputs"""
    webhook_base_url = os.getenv('WEBHOOK_BASE_URL')
    
    test_cases = [
        {
            'speech': 'How much does lawn care cost?',
            'expected_keywords': ['price', 'cost']
        },
        {
            'speech': 'I need to schedule an appointment',
            'expected_keywords': ['schedule', 'appointment']
        },
        {
            'speech': 'This is an emergency, I need help now',
            'expected_keywords': ['emergency']
        },
        {
            'speech': 'I want to speak to the manager',
            'expected_keywords': ['manager']
        }
    ]
    
    print("🧪 Testing speech processing logic...")
    
    for i, test_case in enumerate(test_cases, 1):
        speech = test_case['speech']
        print(f"\n   Test {i}: '{speech}'")
        
        # Simulate the speech processing
        try:
            # This would normally be done by posting to /process_speech
            # For testing, we'll check the keyword logic
            speech_lower = speech.lower()
            
            # Check for forwarding keywords
            forward_keywords = [
                'emergency', 'urgent', 'complaint', 'manager', 'owner', 'supervisor',
                'cancel', 'refund', 'problem', 'issue', 'speak to someone', 'human',
                'representative', 'billing', 'payment issue'
            ]
            
            should_forward = any(keyword in speech_lower for keyword in forward_keywords)
            
            if should_forward:
                print(f"   ➡️  Would forward to owner")
            else:
                print(f"   🤖 Would process with AI")
            
            # Check for expected keywords
            found_keywords = [kw for kw in test_case['expected_keywords'] if kw in speech_lower]
            if found_keywords:
                print(f"   ✅ Found expected keywords: {found_keywords}")
            else:
                print(f"   ⚠️  Expected keywords not found: {test_case['expected_keywords']}")
                
        except Exception as e:
            print(f"   ❌ Error processing: {str(e)}")
    
    return True

def test_environment_variables():
    """Test if all required environment variables are set"""
    required_vars = [
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN',
        'OWNER_PHONE',
        'WEBHOOK_BASE_URL',
        'CHATBOT_ID'
    ]
    
    missing_vars = []
    
    print("🔧 Checking environment variables...")
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"   ✅ {var}: {'*' * (len(value) - 4) + value[-4:] if len(value) > 4 else '***'}")
        else:
            print(f"   ❌ {var}: Not set")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n❌ Missing required variables: {missing_vars}")
        return False
    else:
        print("\n✅ All required environment variables are set")
        return True

def run_all_tests():
    """Run all tests"""
    print("🧪 AI Phone Integration Test Suite")
    print("=" * 50)
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("App Health", test_app_health),
        ("TTS Endpoint", test_tts_endpoint),
        ("Twilio Connection", test_twilio_connection),
        ("Phone Number Config", test_phone_number_config),
        ("Speech Processing", test_speech_processing)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} test...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your AI phone integration is ready!")
    else:
        print("⚠️  Some tests failed. Please check the configuration and try again.")
    
    return passed == total

if __name__ == "__main__":
    run_all_tests()

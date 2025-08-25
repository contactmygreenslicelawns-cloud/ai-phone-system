#!/usr/bin/env python3
"""
Test script to verify AI receptionist deployment
"""
import requests
import sys
from urllib.parse import urljoin

def test_deployment(base_url):
    """Test the deployed AI receptionist"""
    print(f"🧪 Testing deployment at: {base_url}")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(urljoin(base_url, '/health'), timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health check passed")
            print(f"   📊 Status: {data.get('status')}")
            print(f"   🏢 Business: {data.get('business')}")
            print(f"   🤖 Chatbot ID: {data.get('chatbot_id')}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False
    
    # Test 2: TTS test endpoint
    print("\n2. Testing TTS endpoint...")
    try:
        response = requests.get(urljoin(base_url, '/test_tts'), timeout=10)
        if response.status_code == 200 and 'xml' in response.headers.get('content-type', '').lower():
            print(f"   ✅ TTS endpoint working")
            print(f"   📝 Response length: {len(response.text)} chars")
        else:
            print(f"   ❌ TTS endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ TTS endpoint error: {e}")
        return False
    
    # Test 3: Voice webhook (simulate Twilio request)
    print("\n3. Testing voice webhook...")
    try:
        webhook_data = {
            'From': '+15551234567',
            'To': '+15559876543',
            'CallSid': 'test_call_123',
            'AccountSid': 'test_account'
        }
        response = requests.post(
            urljoin(base_url, '/voice'), 
            data=webhook_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=10
        )
        if response.status_code == 200 and 'xml' in response.headers.get('content-type', '').lower():
            print(f"   ✅ Voice webhook working")
            print(f"   📝 TwiML response generated successfully")
            # Check if response contains expected elements
            if 'Gather' in response.text and 'Say' in response.text:
                print(f"   ✅ TwiML contains Gather and Say elements")
            else:
                print(f"   ⚠️  TwiML might be incomplete")
        else:
            print(f"   ❌ Voice webhook failed: {response.status_code}")
            print(f"   📄 Response: {response.text[:200]}...")
            return False
    except Exception as e:
        print(f"   ❌ Voice webhook error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! Your AI receptionist should work.")
    print("\n📋 Next steps:")
    print("1. Update your Twilio webhook URL to point to this deployment")
    print("2. Make sure your Twilio credentials are set in Railway environment variables")
    print("3. Test by calling your Twilio number")
    
    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 test_deployment.py <your-railway-url>")
        print("Example: python3 test_deployment.py https://your-app.up.railway.app")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    if not base_url.startswith('http'):
        base_url = 'https://' + base_url
    
    success = test_deployment(base_url)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

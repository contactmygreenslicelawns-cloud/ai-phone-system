
#!/usr/bin/env python3
"""
Deployment script for AI Phone Integration
Helps set up Twilio phone number and webhooks
"""

import os
import sys
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_twilio_phone_number():
    """Set up Twilio phone number and configure webhooks"""
    
    # Get credentials
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    webhook_base_url = os.getenv('WEBHOOK_BASE_URL')
    
    if not all([account_sid, auth_token, webhook_base_url]):
        print("❌ Missing required environment variables:")
        print("   - TWILIO_ACCOUNT_SID")
        print("   - TWILIO_AUTH_TOKEN") 
        print("   - WEBHOOK_BASE_URL")
        return False
    
    try:
        client = Client(account_sid, auth_token)
        
        print("🔍 Searching for available phone numbers...")
        
        # Search for available phone numbers in the US
        available_numbers = client.available_phone_numbers('US').local.list(
            area_code=None,  # Let Twilio choose
            limit=5
        )
        
        if not available_numbers:
            print("❌ No available phone numbers found")
            return False
        
        print(f"📱 Found {len(available_numbers)} available numbers:")
        for i, number in enumerate(available_numbers):
            print(f"   {i+1}. {number.phone_number} ({number.locality}, {number.region})")
        
        # Let user choose or auto-select first one
        choice = input("\nEnter number to purchase (1-5) or press Enter for first one: ").strip()
        
        if choice and choice.isdigit() and 1 <= int(choice) <= len(available_numbers):
            selected_number = available_numbers[int(choice) - 1]
        else:
            selected_number = available_numbers[0]
        
        print(f"💳 Purchasing {selected_number.phone_number}...")
        
        # Purchase the phone number
        purchased_number = client.incoming_phone_numbers.create(
            phone_number=selected_number.phone_number,
            voice_url=f"{webhook_base_url}/voice",
            voice_method='POST',
            status_callback=f"{webhook_base_url}/call_status",
            status_callback_method='POST'
        )
        
        print(f"✅ Successfully purchased: {purchased_number.phone_number}")
        print(f"📞 Voice webhook: {webhook_base_url}/voice")
        print(f"📊 Status webhook: {webhook_base_url}/call_status")
        
        # Save to .env file
        env_file = '.env'
        if os.path.exists(env_file):
            with open(env_file, 'a') as f:
                f.write(f"\n# Purchased Twilio Number\nTWILIO_PHONE_NUMBER={purchased_number.phone_number}\n")
        
        print(f"\n🎉 Setup complete! Your AI receptionist is ready at: {purchased_number.phone_number}")
        print("\n📋 Next steps:")
        print("   1. Test the number by calling it")
        print("   2. Set up call forwarding from your Visible number")
        print("   3. Update your business listings with the new number")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up phone number: {str(e)}")
        return False

def test_webhooks():
    """Test webhook endpoints"""
    webhook_base_url = os.getenv('WEBHOOK_BASE_URL')
    
    if not webhook_base_url:
        print("❌ WEBHOOK_BASE_URL not set")
        return False
    
    import requests
    
    try:
        # Test health endpoint
        response = requests.get(f"{webhook_base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
        
        # Test TTS endpoint
        response = requests.get(f"{webhook_base_url}/test_tts", timeout=10)
        if response.status_code == 200:
            print("✅ TTS test endpoint working")
        else:
            print(f"❌ TTS test failed: {response.status_code}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Webhook test failed: {str(e)}")
        return False

def main():
    """Main deployment function"""
    print("🚀 AI Phone Integration Deployment Script")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "setup-number":
            setup_twilio_phone_number()
        elif command == "test-webhooks":
            test_webhooks()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: setup-number, test-webhooks")
    else:
        print("Available commands:")
        print("  python deploy.py setup-number    - Purchase and configure Twilio number")
        print("  python deploy.py test-webhooks   - Test webhook endpoints")

if __name__ == "__main__":
    main()

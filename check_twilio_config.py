#!/usr/bin/env python3
"""
Quick diagnostic script to check Twilio configuration
"""
import os
import sys
from dotenv import load_dotenv

def check_twilio_config():
    """Check current Twilio configuration"""
    print("🔍 Twilio Configuration Diagnostic")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Check required variables
    required_vars = {
        'TWILIO_ACCOUNT_SID': os.getenv('TWILIO_ACCOUNT_SID'),
        'TWILIO_AUTH_TOKEN': os.getenv('TWILIO_AUTH_TOKEN'),
        'WEBHOOK_BASE_URL': os.getenv('WEBHOOK_BASE_URL'),
        'OWNER_PHONE': os.getenv('OWNER_PHONE'),
        'BUSINESS_NAME': os.getenv('BUSINESS_NAME'),
        'CHATBOT_ID': os.getenv('CHATBOT_ID')
    }
    
    print("📋 Environment Variables:")
    issues_found = []
    
    for var_name, var_value in required_vars.items():
        if not var_value:
            print(f"   ❌ {var_name}: NOT SET")
            issues_found.append(f"{var_name} is missing")
        elif var_value.startswith('demo_') or var_value == 'your_' or 'localhost' in var_value:
            print(f"   ⚠️  {var_name}: {var_value} (DEMO/PLACEHOLDER VALUE)")
            issues_found.append(f"{var_name} has demo/placeholder value")
        else:
            # Mask sensitive values
            if 'TOKEN' in var_name or 'SID' in var_name:
                masked_value = var_value[:8] + "..." + var_value[-4:] if len(var_value) > 12 else "***"
                print(f"   ✅ {var_name}: {masked_value}")
            else:
                print(f"   ✅ {var_name}: {var_value}")
    
    print("\n🔧 Issues Found:")
    if not issues_found:
        print("   🎉 No issues found with environment variables!")
    else:
        for issue in issues_found:
            print(f"   • {issue}")
    
    print("\n📝 Next Steps:")
    if issues_found:
        print("   1. Update your Railway environment variables with real values")
        print("   2. Get your Twilio Account SID and Auth Token from console.twilio.com")
        print("   3. Set WEBHOOK_BASE_URL to your Railway deployment URL")
        print("   4. Redeploy your Railway app after updating variables")
    else:
        print("   1. Test your deployment with: python3 test_deployment.py <your-railway-url>")
        print("   2. Configure Twilio webhook to point to your Railway URL")
        print("   3. Test by calling your Twilio number")
    
    return len(issues_found) == 0

if __name__ == "__main__":
    success = check_twilio_config()
    sys.exit(0 if success else 1)

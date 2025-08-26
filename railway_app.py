#!/usr/bin/env python3
"""
Railway-optimized version of the AI Phone Integration app
This version is designed to work with Railway's environment and constraints
"""
import os
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration - use demo values as fallbacks for Railway
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', 'demo_account_sid')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', 'demo_auth_token')
CHATBOT_ID = os.getenv('CHATBOT_ID', '3947607fe')
CHATBOT_URL = f"https://apps.abacus.ai/chatllm/{CHATBOT_ID}"
OWNER_PHONE = os.getenv('OWNER_PHONE', '+15551234567')
BUSINESS_NAME = os.getenv('BUSINESS_NAME', 'Green Slice Lawn Care and Window Washing')
WEBHOOK_BASE_URL = os.getenv('WEBHOOK_BASE_URL', 'https://ai-phone-integration-production.up.railway.app')

# Check if we're in demo mode
demo_mode = TWILIO_ACCOUNT_SID == 'demo_account_sid'

@app.route('/')
def index():
    """Root endpoint"""
    return {
        'message': 'AI Phone Integration is running!',
        'status': 'success',
        'mode': 'demo' if demo_mode else 'production',
        'business': BUSINESS_NAME,
        'chatbot_id': CHATBOT_ID,
        'endpoints': {
            'voice': '/voice (POST)',
            'health': '/health (GET)',
            'test_tts': '/test_tts (GET)'
        },
        'timestamp': datetime.now().isoformat()
    }

@app.route('/voice', methods=['POST'])
def handle_incoming_call():
    """Handle incoming voice calls - Railway compatible version"""
    try:
        # Get caller information
        caller_number = request.form.get('From', 'Unknown')
        called_number = request.form.get('To', 'Unknown')
        
        logger.info(f"Incoming call from {caller_number} to {called_number}")
        
        # Create TwiML response
        response = VoiceResponse()
        
        if demo_mode:
            response.say(
                f"Hello! You've reached {BUSINESS_NAME}. This is our AI phone system running in demo mode on Railway. "
                "Thank you for calling! This demonstrates that the deployment is working correctly.",
                voice='Polly.Joanna'
            )
        else:
            response.say(
                f"Hello! You've reached {BUSINESS_NAME}. How can I help you today?",
                voice='Polly.Joanna'
            )
            
            # In production mode, we would gather speech input here
            # For now, just provide a simple response
            response.say(
                "I'm here to help with your lawn care and window washing needs. "
                "Let me connect you with our team.",
                voice='Polly.Joanna'
            )
            
            if OWNER_PHONE and OWNER_PHONE != '+15551234567':
                response.dial(OWNER_PHONE)
        
        return Response(str(response), mimetype='text/xml')
        
    except Exception as e:
        logger.error(f"Error in handle_incoming_call: {str(e)}")
        response = VoiceResponse()
        response.say("I'm sorry, there's a technical issue. Please try calling back later.")
        return Response(str(response), mimetype='text/xml')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'mode': 'demo' if demo_mode else 'production',
        'chatbot_id': CHATBOT_ID,
        'business': BUSINESS_NAME,
        'port': os.environ.get('PORT', 'not set'),
        'webhook_url': WEBHOOK_BASE_URL
    }

@app.route('/test_tts', methods=['GET'])
def test_tts():
    """Test endpoint for TTS"""
    response = VoiceResponse()
    response.say(
        f"This is a test of the {BUSINESS_NAME} AI phone system running on Railway. "
        "Text-to-speech is working correctly!",
        voice='Polly.Joanna'
    )
    return Response(str(response), mimetype='text/xml')

if __name__ == '__main__':
    # Get port from environment variable (Railway sets this automatically)
    port = int(os.environ.get("PORT", 5000))
    
    if demo_mode:
        logger.info(f"Starting AI Phone Integration in DEMO MODE for {BUSINESS_NAME}")
        print("🚀 Demo Mode: AI Phone Integration is running on Railway!")
        print("📞 This is a demonstration version - set real Twilio credentials for production use")
    else:
        logger.info(f"Starting AI Phone Integration for {BUSINESS_NAME}")
    
    print(f"🚀 Starting server on 0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)

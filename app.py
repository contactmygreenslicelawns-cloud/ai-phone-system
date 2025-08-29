from flask import Flask, request, Response
import requests
import os
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
import logging
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration from environment variables
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
CHATBOT_ID = os.getenv('CHATBOT_ID', '3947607fe')  # Your Green Slice chatbot ID
CHATBOT_URL = f"https://apps.abacus.ai/chatllm/{CHATBOT_ID}"
OWNER_PHONE = os.getenv('OWNER_PHONE')  # Phone number to forward calls to
BUSINESS_NAME = os.getenv('BUSINESS_NAME', 'Green Slice Lawn Care and Window Washing')
WEBHOOK_BASE_URL = os.getenv('WEBHOOK_BASE_URL')  # Your deployed app URL

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) if TWILIO_ACCOUNT_SID else None

# Keywords that trigger forwarding to owner
FORWARD_KEYWORDS = [
    'emergency', 'urgent', 'complaint', 'manager', 'owner', 'supervisor',
    'cancel', 'refund', 'problem', 'issue', 'speak to someone', 'human',
    'representative', 'billing', 'payment issue'
]

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return {
        'status': 'AI Phone Integration Active',
        'business': BUSINESS_NAME,
        'endpoints': {
            'voice': '/voice (POST)',
            'health': '/health (GET)',
            'test_tts': '/test_tts (GET)'
        },
        'timestamp': datetime.now().isoformat()
    }

@app.route('/voice', methods=['GET', 'POST'])
def handle_incoming_call():
    """Handle incoming voice calls"""
    # Handle GET requests (for browser testing)
    if request.method == 'GET':
        return "Voice endpoint is ready for Twilio POST requests"
    
    # Handle POST requests (from Twilio)
    try:
        # Get caller information
        caller_number = request.form.get('From', 'Unknown')
        called_number = request.form.get('To', 'Unknown')
        
        logger.info(f"Incoming call from {caller_number} to {called_number}")
        
        # Create TwiML response
        response = VoiceResponse()
        
        # Greet the caller and start gathering speech
        gather = response.gather(
            input='speech',
            action=f'{WEBHOOK_BASE_URL}/process_speech',
            method='POST',
            speech_timeout='auto',
            timeout=10,
            language='en-US',
            hints='lawn care, window washing, cleaning, appointment, quote, pricing'
        )
        
        gather.say(
            f"Hello! Thank you for calling {BUSINESS_NAME}. "
            "I'm your AI assistant. How can I help you today? "
            "Please speak clearly after the tone.",
            voice='Polly.Joanna',
            language='en-US'
        )
        
        # Fallback if no speech detected
        response.say(
            "I didn't hear anything. Let me transfer you to our team.",
            voice='Polly.Joanna'
        )
        response.dial(OWNER_PHONE)
        
        return Response(str(response), mimetype='text/xml')
        
    except Exception as e:
        logger.error(f"Error in handle_incoming_call: {str(e)}")
        response = VoiceResponse()
        response.say("I'm sorry, there's a technical issue. Let me transfer you to our team.")
        if OWNER_PHONE:
            response.dial(OWNER_PHONE)
        return Response(str(response), mimetype='text/xml')

@app.route('/process_speech', methods=['POST'])
def process_speech():
    """Process transcribed speech and generate AI response"""
    try:
        # Get transcribed speech
        speech_result = request.form.get('SpeechResult', '').strip()
        confidence = float(request.form.get('Confidence', 0))
        caller_number = request.form.get('From', 'Unknown')
        
        logger.info(f"Speech from {caller_number}: '{speech_result}' (confidence: {confidence})")
        
        response = VoiceResponse()
        
        # Check if speech was captured with reasonable confidence
        if not speech_result or confidence < 0.3:
            response.say(
                "I'm sorry, I didn't catch that clearly. Let me transfer you to our team for better assistance.",
                voice='Polly.Joanna'
            )
            if OWNER_PHONE:
                response.dial(OWNER_PHONE)
            return Response(str(response), mimetype='text/xml')
        
        # Check for keywords that should trigger immediate forwarding
        if should_forward_to_owner(speech_result):
            logger.info(f"Forwarding call due to keywords in: {speech_result}")
            response.say(
                "I understand you need to speak with someone from our team. Let me connect you right away.",
                voice='Polly.Joanna'
            )
            response.dial(OWNER_PHONE)
            return Response(str(response), mimetype='text/xml')
        
        # Get AI response from Abacus.ai ChatLLM
        ai_response = get_chatbot_response(speech_result, caller_number)
        
        if ai_response:
            # Speak the AI response
            response.say(ai_response, voice='Polly.Joanna', language='en-US')
            
            # Ask for follow-up
            gather = response.gather(
                input='speech',
                action=f'{WEBHOOK_BASE_URL}/process_followup',
                method='POST',
                speech_timeout='auto',
                timeout=8,
                language='en-US'
            )
            gather.say(
                "Is there anything else I can help you with? You can also say 'transfer me' to speak with our team.",
                voice='Polly.Joanna'
            )
            
            # Fallback
            response.say("Thank you for calling. Have a great day!", voice='Polly.Joanna')
        else:
            # Fallback to human if AI fails
            response.say(
                "I'm having trouble processing your request right now. Let me connect you with our team.",
                voice='Polly.Joanna'
            )
            if OWNER_PHONE:
                response.dial(OWNER_PHONE)
        
        return Response(str(response), mimetype='text/xml')
        
    except Exception as e:
        logger.error(f"Error in process_speech: {str(e)}")
        response = VoiceResponse()
        response.say("I'm experiencing technical difficulties. Let me transfer you to our team.")
        if OWNER_PHONE:
            response.dial(OWNER_PHONE)
        return Response(str(response), mimetype='text/xml')

@app.route('/process_followup', methods=['POST'])
def process_followup():
    """Handle follow-up questions"""
    try:
        speech_result = request.form.get('SpeechResult', '').strip()
        caller_number = request.form.get('From', 'Unknown')
        
        logger.info(f"Follow-up from {caller_number}: '{speech_result}'")
        
        response = VoiceResponse()
        
        # Check for transfer requests
        transfer_phrases = ['transfer', 'human', 'person', 'someone', 'representative', 'manager']
        if any(phrase in speech_result.lower() for phrase in transfer_phrases):
            response.say("Of course! Let me connect you with our team right away.", voice='Polly.Joanna')
            if OWNER_PHONE:
                response.dial(OWNER_PHONE)
            return Response(str(response), mimetype='text/xml')
        
        # Check for goodbye/ending phrases
        goodbye_phrases = ['goodbye', 'bye', 'thank you', 'thanks', 'that\'s all', 'nothing else', 'no']
        if any(phrase in speech_result.lower() for phrase in goodbye_phrases):
            response.say(
                f"Thank you for calling {BUSINESS_NAME}! Have a wonderful day!",
                voice='Polly.Joanna'
            )
            return Response(str(response), mimetype='text/xml')
        
        # Process additional question
        if speech_result:
            ai_response = get_chatbot_response(speech_result, caller_number)
            if ai_response:
                response.say(ai_response, voice='Polly.Joanna')
        
        # End the call gracefully
        response.say(
            f"Thank you for calling {BUSINESS_NAME}. If you need further assistance, please call us back. Goodbye!",
            voice='Polly.Joanna'
        )
        
        return Response(str(response), mimetype='text/xml')
        
    except Exception as e:
        logger.error(f"Error in process_followup: {str(e)}")
        response = VoiceResponse()
        response.say("Thank you for calling. Goodbye!")
        return Response(str(response), mimetype='text/xml')

def get_chatbot_response(user_message, caller_number):
    """Get response from Abacus.ai ChatLLM"""
    try:
        # Since we don't have direct API access, we'll simulate the chatbot response
        # In a real implementation, you would make an HTTP request to the Abacus.ai API
        
        # For now, provide intelligent responses based on common lawn care queries
        user_message_lower = user_message.lower()
        
        # Pricing inquiries
        if any(word in user_message_lower for word in ['price', 'cost', 'quote', 'estimate', 'how much']):
            return ("I'd be happy to help with pricing information. Our lawn care services start at $50 per visit, "
                   "and window washing varies by home size. For an accurate quote, I can have our team call you back "
                   "within 2 hours, or you can schedule a free estimate on our website.")
        
        # Scheduling
        elif any(word in user_message_lower for word in ['schedule', 'appointment', 'book', 'when', 'available']):
            return ("I can help you schedule service! We're typically available Monday through Saturday. "
                   "Our next available slots are this week. Would you like me to have someone call you back "
                   "to schedule, or would you prefer to book online?")
        
        # Services
        elif any(word in user_message_lower for word in ['service', 'what do you do', 'lawn', 'window', 'clean']):
            return ("We provide professional lawn care including mowing, edging, and trimming, plus residential "
                   "and commercial window washing. We serve the local area with reliable, quality service. "
                   "What specific service are you interested in?")
        
        # Hours/Contact
        elif any(word in user_message_lower for word in ['hours', 'open', 'contact', 'reach']):
            return ("We're available Monday through Saturday, 8 AM to 6 PM. You can reach us anytime at this number, "
                   "or visit our website. For urgent matters, I can connect you with our team right now.")
        
        # Emergency/Urgent
        elif any(word in user_message_lower for word in ['emergency', 'urgent', 'asap', 'immediately']):
            return ("I understand this is urgent. Let me connect you directly with our team who can help you immediately.")
        
        # Default response
        else:
            return ("Thank you for your question about our lawn care and window washing services. "
                   "I want to make sure you get the best answer. Would you like me to connect you with "
                   "our team for detailed assistance, or is there something specific I can help with?")
            
    except Exception as e:
        logger.error(f"Error getting chatbot response: {str(e)}")
        return None

def should_forward_to_owner(speech_text):
    """Check if the speech contains keywords that should trigger forwarding"""
    speech_lower = speech_text.lower()
    return any(keyword in speech_lower for keyword in FORWARD_KEYWORDS)

@app.route('/call_status', methods=['POST'])
def call_status():
    """Handle call status updates"""
    try:
        call_sid = request.form.get('CallSid')
        call_status = request.form.get('CallStatus')
        from_number = request.form.get('From')
        to_number = request.form.get('To')
        duration = request.form.get('CallDuration', '0')
        
        logger.info(f"Call {call_sid} status: {call_status}, Duration: {duration}s")
        
        # Log call completion
        if call_status == 'completed':
            logger.info(f"Call completed: {from_number} -> {to_number}, Duration: {duration}s")
            
        return Response('OK', mimetype='text/plain')
        
    except Exception as e:
        logger.error(f"Error in call_status: {str(e)}")
        return Response('Error', mimetype='text/plain')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'chatbot_id': CHATBOT_ID,
        'business': BUSINESS_NAME
    }

@app.route('/test_tts', methods=['GET'])
def test_tts():
    """Test endpoint for TTS"""
    response = VoiceResponse()
    response.say(
        f"This is a test of the {BUSINESS_NAME} AI phone system. Text-to-speech is working correctly.",
        voice='Polly.Joanna'
    )
    return Response(str(response), mimetype='text/xml')

if __name__ == '__main__':
    # Validate required environment variables
    required_vars = ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'OWNER_PHONE', 'WEBHOOK_BASE_URL']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    # Check if we have demo values
    demo_mode = os.getenv('TWILIO_ACCOUNT_SID') == 'demo_account_sid'
    
    if missing_vars and not demo_mode:
        logger.error(f"Missing required environment variables: {missing_vars}")
        print(f"Please set the following environment variables: {missing_vars}")
    else:
        if demo_mode:
            logger.info(f"Starting AI Phone Integration in DEMO MODE for {BUSINESS_NAME}")
            print("🚀 Demo Mode: AI Phone Integration is running!")
            print("📞 This is a demonstration version - replace demo credentials with real Twilio credentials for production use")
        else:
            logger.info(f"Starting AI Phone Integration for {BUSINESS_NAME}")
        
        app.run(host='0.0.0.0', port=8080, debug=False)

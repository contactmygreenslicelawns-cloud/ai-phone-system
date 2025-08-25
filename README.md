
# AI Phone Integration for Green Slice Lawn Care & Window Washing

This system integrates your existing Abacus.ai ChatLLM receptionist (ID: 3947607fe) with phone capabilities using Twilio, enabling voice calls with speech-to-text and text-to-speech functionality.

## 🎯 Features

- **Voice-to-Text**: Automatically transcribes caller speech using Twilio's speech recognition
- **Text-to-Voice**: Responds using natural-sounding AI voices
- **Smart Call Routing**: Forwards calls to owner when needed based on keywords or caller requests
- **Call Recording**: Optional call recording and transcription
- **Push Notifications**: Get notified of incoming calls and their status
- **Fallback Handling**: Graceful fallback to human transfer if AI fails

## 🚀 Quick Setup

### 1. Prerequisites

- Twilio account (free trial available)
- Your existing Visible by Verizon phone number
- A server/hosting platform (Render, Heroku, or VPS)

### 2. Installation

```bash
# Clone or download the files
cd ai_phone_integration

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### 3. Configure Environment Variables

Edit `.env` file with your details:

```bash
# Get these from Twilio Console (https://console.twilio.com)
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here

# Your business phone number (where calls should be forwarded)
OWNER_PHONE=+15551234567

# Your deployed app URL (see deployment section)
WEBHOOK_BASE_URL=https://your-app-domain.com

# Business name for greetings
BUSINESS_NAME=Green Slice Lawn Care and Window Washing
```

### 4. Deploy the Application

#### Option A: Deploy to Render (Recommended - Free)

1. Create account at [render.com](https://render.com)
2. Connect your GitHub repository
3. Create new Web Service
4. Set environment variables in Render dashboard
5. Deploy

#### Option B: Deploy to Heroku

```bash
# Install Heroku CLI
heroku create your-app-name
heroku config:set TWILIO_ACCOUNT_SID=your_sid
heroku config:set TWILIO_AUTH_TOKEN=your_token
heroku config:set OWNER_PHONE=+15551234567
heroku config:set WEBHOOK_BASE_URL=https://your-app-name.herokuapp.com
git push heroku main
```

#### Option C: Local Testing with ngrok

```bash
# Install ngrok
pip install pyngrok

# Run the app
python app.py

# In another terminal, expose it
ngrok http 5000

# Use the ngrok URL as your WEBHOOK_BASE_URL
```

### 5. Purchase and Configure Twilio Phone Number

```bash
# After deployment, run the setup script
python deploy.py setup-number
```

This will:
- Purchase a Twilio phone number
- Configure voice webhooks
- Set up call status tracking

### 6. Set Up Call Forwarding from Visible

Forward calls from your existing Visible by Verizon number to your new Twilio number:

#### Method 1: Using Star Codes (Recommended)
```
*72 + [Your Twilio Number]
```
Example: `*72-555-123-4567`

#### Method 2: Conditional Forwarding (Busy/No Answer)
```
*71 + [Your Twilio Number]
```

#### To Disable Forwarding
```
*73
```

### 7. Test the System

1. Call your Twilio number directly to test AI responses
2. Call your original Visible number to test forwarding
3. Try different scenarios:
   - Ask about pricing
   - Request to speak to someone
   - Ask about services
   - Say "emergency" to test immediate forwarding

## 📞 How It Works

1. **Call Received**: Twilio receives the forwarded call
2. **Greeting**: AI greets caller and asks how it can help
3. **Speech Recognition**: Caller's speech is transcribed
4. **AI Processing**: System generates appropriate response
5. **Text-to-Speech**: Response is spoken back to caller
6. **Smart Routing**: Calls are forwarded to owner when needed

## 🔧 Configuration Options

### Call Forwarding Keywords

The system automatically forwards calls when these keywords are detected:
- emergency, urgent, complaint
- manager, owner, supervisor
- cancel, refund, problem, issue
- speak to someone, human, representative
- billing, payment issue

### Voice Settings

Customize the AI voice in `app.py`:
```python
# Change voice (options: Polly.Joanna, Polly.Matthew, woman, man)
voice='Polly.Joanna'

# Change language
language='en-US'
```

### Business Responses

Modify responses in the `get_chatbot_response()` function to match your business needs.

## 📊 Monitoring and Analytics

### Call Logs
Check your Twilio Console for:
- Call duration and status
- Speech transcription accuracy
- Error logs

### Health Check
Visit `https://your-app-domain.com/health` to verify system status.

### Test Endpoints
- `/test_tts` - Test text-to-speech functionality
- `/health` - System health check

## 💰 Pricing

### Twilio Costs (Pay-as-you-go)
- Phone number: ~$1/month
- Incoming calls: ~$0.0085/minute
- Speech-to-text: ~$0.02/minute
- Text-to-speech: ~$0.04/1000 characters

### Hosting Costs
- Render: Free tier available
- Heroku: Free tier available
- VPS: $5-20/month

**Estimated monthly cost for 100 calls (5 min avg): ~$10-15**

## 🔒 Security Features

- Environment variable protection
- Webhook validation
- Call recording encryption
- No sensitive data logging

## 🆘 Troubleshooting

### Common Issues

**"Call forwarding not working"**
- Verify star code: `*72+[Twilio number]`
- Check Visible account settings
- Ensure Twilio number supports voice

**"AI not responding"**
- Check webhook URL in Twilio console
- Verify app is deployed and running
- Check environment variables

**"Poor speech recognition"**
- Ensure clear audio quality
- Check for background noise
- Verify language settings

**"Calls not forwarding to owner"**
- Verify OWNER_PHONE format: `+1234567890`
- Check Twilio account balance
- Test with direct dial

### Getting Help

1. Check Twilio Console logs
2. Review app logs in hosting platform
3. Test individual endpoints
4. Contact support with specific error messages

## 📱 Advanced Features

### Call Recording
Enable in `.env`:
```bash
ENABLE_CALL_RECORDING=true
```

### Push Notifications
Set up webhook for call notifications:
```bash
PUSH_NOTIFICATION_URL=https://your-notification-service.com/webhook
```

### Custom Responses
Integrate with your actual Abacus.ai ChatLLM API by modifying the `get_chatbot_response()` function.

## 🔄 Updates and Maintenance

### Regular Tasks
- Monitor call quality and transcription accuracy
- Update business responses as needed
- Check Twilio usage and billing
- Test call forwarding monthly

### Scaling
- Add multiple phone numbers for different regions
- Implement call queuing for high volume
- Add SMS integration
- Create admin dashboard

## 📞 Support

For technical support:
1. Check the troubleshooting section
2. Review Twilio documentation
3. Contact your hosting provider
4. Reach out to Abacus.ai support for ChatLLM issues

---

**Your AI receptionist is now ready to handle calls 24/7!** 🎉

Test it thoroughly and adjust the responses to match your business needs.

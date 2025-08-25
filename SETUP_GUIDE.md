# 🚀 Complete Setup Guide: AI Phone Integration for Green Slice Lawn Care

## 📋 What You'll Get

Your AI receptionist will be able to:
- ✅ Answer calls 24/7 with natural voice responses
- ✅ Handle common questions about lawn care and window washing
- ✅ Schedule appointments and provide pricing information
- ✅ Forward urgent calls or specific requests to you
- ✅ Record and transcribe all conversations
- ✅ Send you notifications about calls

## 🎯 Step-by-Step Setup

### Phase 1: Get Your Twilio Account Ready (15 minutes)

1. **Create Twilio Account**
   - Go to https://www.twilio.com/try-twilio
   - Sign up for a free account ($15 credit included)
   - Verify your phone number

2. **Get Your Credentials**
   - Go to https://console.twilio.com
   - Copy your Account SID and Auth Token
   - Keep these safe - you'll need them soon

### Phase 2: Deploy Your AI System (20 minutes)

**Option A: Deploy to Render (Recommended - Free)**

1. Create account at https://render.com
2. Fork this code to your GitHub account
3. Connect GitHub to Render
4. Create new "Web Service"
5. Set these environment variables in Render:
   ```
   TWILIO_ACCOUNT_SID=your_actual_account_sid
   TWILIO_AUTH_TOKEN=your_actual_auth_token
   OWNER_PHONE=+1234567890  (your cell number)
   WEBHOOK_BASE_URL=https://your-app-name.onrender.com
   BUSINESS_NAME=Green Slice Lawn Care and Window Washing
   CHATBOT_ID=3947607fe
   ```
6. Deploy the service

**Option B: Deploy to Heroku**

```bash
# Install Heroku CLI, then:
heroku create your-app-name
heroku config:set TWILIO_ACCOUNT_SID=your_sid
heroku config:set TWILIO_AUTH_TOKEN=your_token
heroku config:set OWNER_PHONE=+1234567890
heroku config:set WEBHOOK_BASE_URL=https://your-app-name.herokuapp.com
git push heroku main
```

### Phase 3: Get Your AI Phone Number (10 minutes)

1. **Purchase Twilio Number**
   ```bash
   python deploy.py setup-number
   ```
   This will:
   - Show you available phone numbers
   - Let you choose one
   - Automatically configure it for your AI system
   - Cost: ~$1/month

2. **Test Your AI System**
   - Call your new Twilio number
   - Try saying: "How much does lawn care cost?"
   - Try saying: "I need to speak to the manager" (should forward to you)

### Phase 4: Forward Your Existing Number (5 minutes)

**From your Visible by Verizon phone:**

**For Business Hours (Recommended):**
```
*71 + [Your Twilio Number]
```
Example: `*71-555-123-4567`

This forwards calls only when you're busy or don't answer.

**For After Hours:**
```
*72 + [Your Twilio Number]
```
This forwards ALL calls immediately to AI.

**To Turn Off Forwarding:**
```
*73
```

## 🧪 Testing Your Setup

### Test Scenarios

1. **Basic Service Inquiry**
   - Call and ask: "What services do you offer?"
   - Expected: AI explains lawn care and window washing services

2. **Pricing Question**
   - Ask: "How much does it cost?"
   - Expected: AI provides pricing information and offers callback

3. **Scheduling Request**
   - Say: "I want to schedule service"
   - Expected: AI offers to have someone call back or book online

4. **Emergency/Urgent Transfer**
   - Say: "This is an emergency" or "I need to speak to someone"
   - Expected: AI immediately transfers to your phone

5. **After Hours Test**
   - Call outside business hours
   - Expected: AI handles professionally and offers next-day callback

## 📊 Monitoring Your System

### Daily Checks
- Visit: `https://your-app-domain.com/health`
- Check Twilio Console for call logs
- Review any missed calls or errors

### Weekly Reviews
- Analyze call transcripts for improvement opportunities
- Update AI responses based on common questions
- Check call forwarding is working correctly

## 💰 Cost Breakdown

### Monthly Costs
- **Twilio Phone Number**: $1.00/month
- **Incoming Calls**: ~$0.0085/minute
- **Speech Recognition**: ~$0.02/minute  
- **Text-to-Speech**: ~$0.04/1000 characters
- **Hosting (Render/Heroku)**: Free tier available

### Example: 100 calls/month (5 min average)
- Phone number: $1.00
- Call time: $4.25 (500 minutes × $0.0085)
- Speech processing: $10.00 (500 minutes × $0.02)
- Text-to-speech: $2.00 (estimated)
- **Total: ~$17.25/month**

## 🔧 Customization Options

### Modify AI Responses
Edit the `get_chatbot_response()` function in `app.py`:

```python
# Add your specific pricing
if 'price' in user_message_lower:
    return "Our lawn care starts at $50 per visit. Window washing is $3 per window. Would you like a free estimate?"

# Add your service areas
if 'area' in user_message_lower or 'location' in user_message_lower:
    return "We serve [Your City] and surrounding areas within 20 miles. What's your address?"
```

### Change Voice Settings
```python
# In app.py, change the voice:
voice='Polly.Matthew'  # Male voice
voice='Polly.Joanna'   # Female voice (default)
language='en-US'       # US English
```

### Add More Forward Keywords
```python
FORWARD_KEYWORDS = [
    'emergency', 'urgent', 'complaint', 'manager', 'owner',
    'cancel', 'refund', 'problem', 'billing',
    # Add your custom keywords:
    'estimate', 'quote', 'schedule today'
]
```

## 🆘 Troubleshooting

### "Calls aren't being forwarded"
- Check: Dialed `*71` + full 10-digit number?
- Check: Twilio number configured correctly?
- Test: Call Twilio number directly first

### "AI isn't responding properly"
- Check: App health at `/health` endpoint
- Check: Twilio Console webhook logs
- Check: Environment variables set correctly

### "Poor call quality"
- Check: Good cell signal when testing
- Check: Background noise during calls
- Consider: Different Twilio voice options

### "Calls going to voicemail instead of AI"
- Check: Call forwarding activated (`*71` or `*72`)
- Check: Twilio number supports voice calls
- Check: Webhook URLs are correct

## 📞 Support Contacts

### Technical Issues
1. Check this troubleshooting guide
2. Review Twilio Console logs
3. Test individual endpoints
4. Check hosting platform logs

### Twilio Support
- Console: https://console.twilio.com
- Documentation: https://www.twilio.com/docs
- Support: Available in Twilio Console

### Hosting Support
- **Render**: https://render.com/docs
- **Heroku**: https://devcenter.heroku.com

## 🔄 Maintenance Schedule

### Weekly
- [ ] Test call forwarding
- [ ] Review call transcripts
- [ ] Check system health
- [ ] Update AI responses if needed

### Monthly
- [ ] Review Twilio usage and costs
- [ ] Test all call scenarios
- [ ] Update business information
- [ ] Check for system updates

### Quarterly
- [ ] Analyze call patterns
- [ ] Optimize AI responses
- [ ] Review and update pricing information
- [ ] Consider additional features

## 🚀 Advanced Features (Optional)

### SMS Integration
Add text message capabilities to your AI system.

### Multiple Phone Numbers
Set up different numbers for different services or locations.

### Call Analytics Dashboard
Create a web dashboard to view call statistics and trends.

### CRM Integration
Connect calls to your customer management system.

### Appointment Scheduling
Integrate with calendar systems for automatic booking.

---

## 🎉 You're All Set!

Your AI receptionist is now ready to handle calls professionally 24/7. 

**Next Steps:**
1. Test thoroughly with different scenarios
2. Update your business listings with the new number
3. Train your team on the forwarding system
4. Monitor and optimize based on real calls

**Questions?** Review the troubleshooting section or check the detailed README.md file.

---

*Your customers will be impressed with the professional, always-available service!*

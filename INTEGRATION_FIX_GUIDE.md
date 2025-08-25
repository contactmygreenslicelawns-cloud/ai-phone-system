# 🔧 AI Receptionist Integration Fix Guide

## 🚨 **Current Issues Identified**

Your AI receptionist is failing because:
1. **Demo credentials** in environment variables instead of real Twilio credentials
2. **Wrong webhook URL** pointing to localhost instead of Railway deployment
3. **Twilio webhook configuration** not pointing to the correct endpoint

## ✅ **Step-by-Step Solution**

### **Phase 1: Get Your Railway URL**

1. **Login to Railway Dashboard**
   - Go to [railway.app](https://railway.app)
   - Find your AI phone integration project
   - Copy the deployment URL (looks like: `https://your-app-name.up.railway.app`)

2. **Test if Railway App is Running**
   ```bash
   # Replace with your actual Railway URL
   python3 test_deployment.py https://your-app-name.up.railway.app
   ```

### **Phase 2: Update Railway Environment Variables**

In your Railway project dashboard:

1. **Go to Variables tab**
2. **Delete or update these variables:**
   ```
   TWILIO_ACCOUNT_SID=your_real_account_sid_from_twilio_console
   TWILIO_AUTH_TOKEN=your_real_auth_token_from_twilio_console
   WEBHOOK_BASE_URL=https://your-app-name.up.railway.app
   OWNER_PHONE=+1234567890  # Your real phone number
   ```

3. **Keep these as they are:**
   ```
   BUSINESS_NAME=Green Slice Lawn Care and Window Washing
   CHATBOT_ID=3947607fe
   ENABLE_CALL_RECORDING=true
   ```

### **Phase 3: Get Real Twilio Credentials**

1. **Login to Twilio Console**
   - Go to [console.twilio.com](https://console.twilio.com)
   - Dashboard → Account Info section

2. **Copy Your Credentials:**
   - **Account SID**: Starts with "AC..." (about 34 characters)
   - **Auth Token**: Click "Show" to reveal (about 32 characters)

### **Phase 4: Configure Twilio Webhook**

1. **Go to Phone Numbers**
   - Twilio Console → Phone Numbers → Manage → Active numbers
   - Click on your Twilio phone number

2. **Set Voice Webhook:**
   - **URL**: `https://your-app-name.up.railway.app/voice`
   - **HTTP Method**: POST
   - **Primary Handler Fails**: Leave blank or set fallback URL

3. **Set Status Callback (Optional):**
   - **URL**: `https://your-app-name.up.railway.app/call_status`
   - **HTTP Method**: POST

4. **Save Configuration**

### **Phase 5: Test the Integration**

1. **Test Deployment Health:**
   ```bash
   curl https://your-app-name.up.railway.app/health
   ```
   Should return JSON with status "healthy"

2. **Test Voice Endpoint:**
   ```bash
   curl -X POST https://your-app-name.up.railway.app/voice \
     -d "From=+15551234567" \
     -d "To=+15559876543" \
     -d "CallSid=test123"
   ```
   Should return TwiML XML

3. **Call Your Twilio Number:**
   - Dial your Twilio phone number
   - Should hear: "Hello! Thank you for calling Green Slice Lawn Care..."

## 🔍 **Debugging Common Issues**

### **Issue 1: "Webhook Error 11200 or 11205"**
**Cause**: Twilio can't reach your webhook URL
**Solution**:
- Verify Railway app is deployed and running
- Check webhook URL is exactly: `https://your-app-name.up.railway.app/voice`
- Test URL accessibility from external network

### **Issue 2: "Call Connects but No Voice Response"**
**Cause**: Environment variables not set correctly
**Solution**:
- Check Railway environment variables are saved
- Redeploy after changing variables
- Check Railway logs for errors

### **Issue 3: "App Crashes on Call"**
**Cause**: Missing dependencies or code errors
**Solution**:
- Check Railway deployment logs
- Ensure all packages in requirements.txt are installed
- Look for Python errors in logs

### **Issue 4: "Immediate Transfer to Owner Phone"**
**Cause**: AI processing failing, triggering fallback
**Solution**:
- Check if OWNER_PHONE is set correctly
- Verify speech processing is working
- Check Railway logs for AI response errors

## 📋 **Verification Checklist**

Before testing, ensure:

- [ ] Railway app is deployed and accessible
- [ ] Real Twilio credentials (not demo) are set in Railway
- [ ] WEBHOOK_BASE_URL points to Railway URL (not localhost)
- [ ] Twilio phone number webhook points to Railway `/voice` endpoint
- [ ] OWNER_PHONE is set to your real phone number
- [ ] Railway app health endpoint returns 200 OK

## 🧪 **Testing Commands**

Use these commands to test each component:

```bash
# 1. Test Railway deployment
python3 test_deployment.py https://your-app-name.up.railway.app

# 2. Test health endpoint
curl https://your-app-name.up.railway.app/health

# 3. Test TTS endpoint
curl https://your-app-name.up.railway.app/test_tts

# 4. Test voice webhook
curl -X POST https://your-app-name.up.railway.app/voice \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "From=+15551234567&To=+15559876543&CallSid=test123"
```

## 🆘 **If Still Not Working**

1. **Check Twilio Debugger:**
   - Go to Twilio Console → Monitor → Debugger
   - Look for recent errors with your phone number
   - Copy error details

2. **Check Railway Logs:**
   - Railway Dashboard → Your Project → Deployments
   - Click on latest deployment → View Logs
   - Look for Python errors or HTTP request logs

3. **Test with ngrok (Local Development):**
   ```bash
   # In one terminal
   cd /home/ubuntu/ai_phone_integration
   python3 app.py

   # In another terminal
   ngrok http 5000
   ```
   Use the ngrok URL temporarily in Twilio webhook to test locally

## 📞 **Expected Call Flow**

When working correctly:
1. **Call Twilio number** → Twilio sends POST to `/voice`
2. **AI greets caller** → "Hello! Thank you for calling Green Slice..."
3. **Caller speaks** → Twilio transcribes and sends to `/process_speech`
4. **AI responds** → Intelligent response based on query
5. **Follow-up or transfer** → Continues conversation or transfers to owner

## 🎯 **Success Indicators**

✅ Railway health endpoint returns 200  
✅ Voice webhook returns valid TwiML  
✅ Twilio Debugger shows no errors  
✅ Call connects and AI speaks greeting  
✅ Speech recognition and AI responses work  
✅ Transfer to owner phone works when requested  

---

**Need Help?** 
- Check Railway deployment logs for errors
- Use Twilio Debugger to see webhook request/response details
- Test each endpoint individually using the commands above

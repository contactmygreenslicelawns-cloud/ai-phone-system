
# Call Forwarding Setup Instructions

## Setting Up Call Forwarding from Visible by Verizon to Your AI Receptionist

### Step 1: Get Your Twilio Phone Number

After deploying your AI phone integration, you'll have a Twilio phone number. This is where calls will be forwarded to.

**To find your Twilio number:**
1. Run: `python deploy.py setup-number` (if you haven't already)
2. Or check your Twilio Console at https://console.twilio.com
3. Note down the number (format: +1-XXX-XXX-XXXX)

### Step 2: Set Up Call Forwarding on Visible

#### Option A: Immediate Call Forwarding (All Calls)
This forwards ALL incoming calls immediately to your AI system.

**From your Visible phone, dial:**
```
*72[Twilio Number]
```

**Example:**
If your Twilio number is +1-555-123-4567, dial:
```
*725551234567
```

**What happens:**
- Your phone won't ring
- All calls go directly to AI receptionist
- Callers don't know they're being forwarded

#### Option B: Conditional Call Forwarding (Recommended)
This forwards calls only when you're busy or don't answer.

**From your Visible phone, dial:**
```
*71[Twilio Number]
```

**Example:**
```
*715551234567
```

**What happens:**
- Your phone rings first (3-6 rings)
- If you don't answer or are busy, calls forward to AI
- You can still take calls normally when available

#### Option C: No Answer Call Forwarding
Forwards only when you don't answer (not when busy).

**From your Visible phone, dial:**
```
*61[Twilio Number]
```

### Step 3: Confirm Setup

After dialing the forwarding code:
1. Listen for confirmation beeps or tone
2. Hang up when you hear the confirmation
3. Test by having someone call your Visible number

### Step 4: Test the Integration

**Test Scenarios:**
1. **Basic Test**: Have someone call and ask about services
2. **Forwarding Test**: Say "I need to speak to the manager"
3. **Emergency Test**: Say "This is an emergency"
4. **Pricing Test**: Ask "How much does lawn care cost?"

### Step 5: Disable Call Forwarding (If Needed)

**To turn off all call forwarding:**
```
*73
```

**To change forwarding settings:**
1. First dial `*73` to disable current forwarding
2. Then set up new forwarding with desired option

## Advanced Forwarding Options

### Time-Based Forwarding
Set up different forwarding for business hours vs. after hours:

**Business Hours (8 AM - 6 PM):**
- Use conditional forwarding (*71) so you can answer directly
- AI handles overflow and after-hours

**After Hours:**
- Use immediate forwarding (*72) so all calls go to AI
- AI can take messages or handle urgent requests

### Selective Forwarding
Forward only specific types of calls:

**For VIP customers:**
- Give them your direct Visible number
- Use conditional forwarding so you can prioritize their calls

**For general inquiries:**
- Advertise your Twilio number directly
- All calls go straight to AI receptionist

## Troubleshooting Call Forwarding

### Common Issues

**"Forwarding not working"**
- Ensure you dialed the complete number without spaces or dashes
- Try again with exact format: `*72` + 10-digit number
- Check that your Visible plan includes call forwarding

**"Getting busy signal"**
- Your Twilio number might not be configured correctly
- Check webhook settings in Twilio Console
- Verify your app is running and accessible

**"Calls not reaching AI"**
- Test your Twilio number directly first
- Check app logs for errors
- Verify webhook URLs are correct

**"Can't disable forwarding"**
- Try `*73` multiple times
- Contact Visible support if needed
- May need to wait a few minutes between attempts

### Visible-Specific Notes

- Call forwarding is included in most Visible plans
- No additional charges for forwarding within the US
- International forwarding may not be supported
- Some features may require account verification

### Testing Checklist

- [ ] Forwarding code dialed successfully (heard confirmation)
- [ ] Test call reaches AI receptionist
- [ ] AI responds appropriately to questions
- [ ] Emergency keywords trigger human transfer
- [ ] Call quality is acceptable
- [ ] Forwarding can be disabled with *73

## Business Hour Recommendations

### Recommended Setup for Green Slice Lawn Care

**During Business Hours (Monday-Saturday, 8 AM - 6 PM):**
```
*71[Twilio Number]  # Conditional forwarding
```
- You can answer calls directly when available
- AI handles calls when you're busy or with customers
- Provides backup so no calls are missed

**After Hours and Weekends:**
```
*72[Twilio Number]  # Immediate forwarding
```
- All calls go to AI for after-hours service
- AI can schedule appointments for next business day
- Emergency calls still get forwarded to you

**To switch between modes:**
1. Dial `*73` to disable current forwarding
2. Dial new forwarding code
3. Test with a call

### Pro Tips

1. **Update Your Voicemail**: Change your Visible voicemail to mention the AI service
2. **Business Cards**: You can use either number on marketing materials
3. **Google My Business**: Update with your preferred number
4. **Monitor Performance**: Check call logs weekly to optimize responses

---

**Your AI receptionist is now ready to handle calls professionally 24/7!**

For technical support, check the main README.md or contact your system administrator.

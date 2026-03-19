# Email & WhatsApp Messaging Setup Guide

## 🎉 What's New!

Your StudentManager now has **free email and WhatsApp messaging**!

### Features Added:
- ✉️ **Email Notifications** (via Gmail - 500 emails/day free)
- 💬 **WhatsApp Click-to-Chat** (100% free, no API needed)
- 📨 **Message Templates** (welcome, attendance, reports, receipts)
- 📊 **Messaging Dashboard** (manage all communications)

---

## 📧 Email Setup (5 minutes)

### Step 1: Enable Gmail App Password

1. Go to your Google Account: https://myaccount.google.com/
2. Enable **2-Step Verification** (if not already enabled)
3. Go to **App Passwords**: https://myaccount.google.com/apppasswords
4. Select **Mail** and your device
5. Copy the **16-character password**

### Step 2: Configure .env File

Edit your `.env` file (or create from `.env.example`):

```bash
# Email Configuration (Gmail SMTP - Free)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USE_SSL=false
MAIL_USERNAME=your-email@gmail.com      # Your Gmail address
MAIL_PASSWORD=abcd-efgh-ijkl-mnop       # 16-char App Password
MAIL_DEFAULT_SENDER=your-email@gmail.com
MAIL_ADMIN=admin@example.com
```

### Step 3: Test Email

1. Restart your app
2. Go to **Messaging** in sidebar
3. Click envelope icon next to any student
4. Select "Welcome Email" and send!

---

## 💬 WhatsApp Setup (Instant!)

### No Setup Required!

WhatsApp messaging works **immediately** - no configuration needed!

### How It Works:

1. Click the **WhatsApp icon** 📱 next to any student's phone number
2. WhatsApp Web opens with pre-filled message
3. Click send in WhatsApp

### Customize Country Code (Optional)

Edit `.env`:
```bash
WHATSAPP_COUNTRY_CODE=254  # Kenya
# Other codes: 234=Nigeria, 27=South Africa, 91=India, etc.
```

---

## 📨 Email Templates Available

### 1. Welcome Email
- Sent when: New student enrolled
- Contains: Course details, modules, enrollment info
- Trigger: Manual or auto on enrollment

### 2. Attendance Alert
- Sent when: Attendance < 70%
- Contains: Current attendance rate, statistics
- Trigger: Manual or auto-alerts

### 3. Monthly Progress Report
- Sent when: End of month
- Contains: Attendance, performance, payment status
- Trigger: Manual (one-click send)

### 4. Payment Receipt
- Sent when: Payment recorded
- Contains: Payment details, total paid, balance
- Trigger: Auto on payment (coming soon)

### 5. Certificate Ready
- Sent when: Certificate generated
- Contains: Certificate details, download info
- Trigger: Auto on generation (coming soon)

---

## 🚀 Using the Messaging Center

### Access Messaging

1. Click **Messaging** in sidebar
2. See all students with quick actions

### Send Individual Email

1. Click envelope icon ✉️ next to student
2. Select email type
3. Review preview
4. Click "Send Email"

### Send WhatsApp Message

1. Click WhatsApp icon 📱 next to student
2. WhatsApp opens with pre-filled message
3. Click send in WhatsApp

### Bulk Email (Low Attendance)

1. Click "Send Low Attendance Alerts" button
2. Emails sent to all students with <70% attendance
3. Done!

---

## 📊 Features by Channel

| Feature | Email | WhatsApp | SMS |
|---------|-------|----------|-----|
| **Cost** | Free | Free | Paid |
| **Setup** | 5 min | None | 10 min |
| **Rich Content** | ✅ Yes | ✅ Yes | ❌ Text only |
| **Attachments** | ✅ PDF | ✅ Images | ❌ No |
| **Delivery Tracking** | ✅ Yes | ❌ Manual | ✅ Yes |
| **Two-way** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Best For** | Reports, Receipts | Quick alerts | Urgent only |

---

## 🔧 Troubleshooting

### Email Not Sending?

**Check:**
1. Gmail App Password (not regular password)
2. 2-Step Verification enabled
3. `.env` file configured correctly
4. Restart app after config changes

**Test:**
```bash
flask shell
>>> from email_service import send_email
>>> send_email('Test', 'your-email@gmail.com', 'Test body', '<b>Test HTML</b>')
```

### WhatsApp Not Opening?

**Check:**
1. Student has phone number
2. Phone number format (include country code)
3. WhatsApp Web installed on computer OR WhatsApp mobile app

**Fix:**
- Edit student and add phone with country code
- Example: `+254712345678` or `0712345678` (auto-converts)

---

## 💡 Best Practices

### Email
- ✅ Use for formal communications
- ✅ Attach PDFs (reports, certificates)
- ✅ Send monthly progress updates
- ❌ Don't overuse (max 500/day Gmail limit)

### WhatsApp
- ✅ Use for quick alerts
- ✅ Send attendance reminders
- ✅ Share photos (certificates, events)
- ✅ Two-way communication
- ❌ Don't spam

### SMS (Twilio - Paid)
- ✅ Emergency alerts only
- ✅ Critical notifications
- ❌ Don't use for regular comms (costly)

---

## 📈 What's Next?

### Coming Soon (Auto-Triggers):
- [ ] Auto-send welcome email on student enrollment
- [ ] Auto-send payment receipt on payment
- [ ] Auto-send certificate on generation
- [ ] Scheduled monthly reports
- [ ] Email analytics (open rate, click rate)

### Want More?
- Email templates customization
- Bulk SMS via Twilio
- WhatsApp Business API (automated)
- Push notifications (web/mobile app)

---

## 🎯 Quick Reference

### Gmail App Password Setup
https://support.google.com/accounts/answer/185833

### WhatsApp Click-to-Chat
https://faq.whatsapp.com/general/chats/how-to-use-click-to-chat

### Country Codes
https://countrycode.org/

---

**Enjoy your free messaging system! 🎉**

Questions? Check the messaging dashboard or contact support.

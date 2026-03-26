# Messaging Setup Guide

This guide covers email and WhatsApp messaging features.

---

## Email Notifications

### Overview

The system provides **two email sending options** - both require **NO server configuration**:

1. **Send via Gmail** - Opens Gmail compose in your browser
2. **Open Email App** - Opens your default email client (Outlook, Apple Mail, etc.)

### Features

✅ **No SMTP Configuration Required**
- No Gmail App Password needed
- No server-side email setup
- Uses your personal Gmail account

✅ **Pre-filled Messages**
- Student email auto-filled
- Subject line pre-populated
- Message body template included

✅ **Bulk Email Support**
- Send to multiple students at once
- Attendance alerts
- Custom messages

### How to Use

#### Individual Student Email

1. Go to **Messaging** → Find student
2. Click **"Message"** dropdown
3. Choose:
   - **"Send via Gmail"** → Opens Gmail compose
   - **"Open Email App"** → Opens email client

#### Bulk Attendance Alerts

1. Go to **Messaging**
2. Click **"Send Low Attendance Alerts"**
3. View students with attendance < 50%
4. Choose:
   - **"Send via Gmail"** → Opens Gmail with all students
   - **"Send via Email App"** → Opens email client with all students

### Email Templates

#### Attendance Alert
```
Subject: Attendance Alert - COLMAC Computer College

Dear Student/Parent,

This is to inform you that the student's attendance is below the required 50%.

Please ensure regular attendance to qualify for the certificate.

Best regards,
COLMAC Computer College
```

---

## WhatsApp Messaging

### Overview

Free WhatsApp integration using **Click-to-Chat** - no API required!

### Features

✅ **Completely Free**
- No WhatsApp Business API
- No monthly fees
- No message limits

✅ **Easy to Use**
- Click button → Opens WhatsApp
- Pre-filled message
- Send from your phone

✅ **Works Everywhere**
- Mobile phones
- Desktop WhatsApp
- WhatsApp Web

### How to Use

#### Individual Student

1. Go to **Messaging** → Find student
2. Click **"Message"** dropdown
3. Click **"Send WhatsApp"**
4. WhatsApp opens with pre-filled message
5. Send from your phone

#### Message Templates

**Welcome Message:**
```
Hello [Student Name], welcome to COLMAC Computer College!
```

**Attendance Reminder:**
```
Dear Student, your attendance is below 50%. Please attend classes regularly to complete your course successfully.
```

**Payment Reminder:**
```
Dear Student, you have an outstanding fee balance. Please complete your payment to continue your studies.
```

---

## Comparison: Email vs WhatsApp

| Feature | Email | WhatsApp |
|---------|-------|----------|
| **Cost** | Free | Free |
| **Setup** | None | None |
| **Best For** | Formal communications | Quick reminders |
| **Delivery** | Asynchronous | Instant |
| **Media** | Attachments supported | Images, voice notes |
| **Open Rate** | Medium | High |

---

## Best Practices

### Email

✅ **Do:**
- Use for formal communications
- Include clear subject lines
- Keep messages concise
- Use templates for consistency

❌ **Don't:**
- Send too many emails (avoid spam)
- Use for urgent matters
- Send large attachments

### WhatsApp

✅ **Do:**
- Keep messages short
- Use for urgent reminders
- Send during business hours
- Personalize messages

❌ **Don't:**
- Send too frequently
- Use for formal communications
- Send late at night

---

## Troubleshooting

### Email Not Opening

**Problem:** Gmail/Email App doesn't open

**Solution:**
1. Check if you're logged into Gmail
2. Set a default email client in your OS
3. Try the other option (Gmail vs Email App)

### WhatsApp Not Opening

**Problem:** WhatsApp doesn't open

**Solution:**
1. Install WhatsApp on your phone
2. Ensure phone number is valid
3. Check internet connection

### Message Not Pre-filling

**Problem:** Message body is empty

**Solution:**
1. Check browser pop-up blocker
2. Try a different browser
3. Clear browser cache

---

## Advanced: Server-Side Email (Optional)

If you want automated server-side email (not recommended):

### Gmail SMTP Setup

1. Enable 2-Factor Authentication on Gmail
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Add to `.env`:
   ```
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

**Note:** This is **optional** and **not required** for normal operation. The Gmail web integration works perfectly without any configuration.

---

## Support

For messaging issues:
- Check browser pop-up settings
- Ensure WhatsApp is installed
- Verify email client is configured

Need help? Contact the administrator.

# Payment Tracking Guide

## Overview

The Payment Tracking system allows you to track course fee payments for all students, view payment status, and monitor outstanding balances.

## Features

### Payment Dashboard

The main payments page shows:

1. **Summary Cards**
   - Total Revenue: All payments received
   - Pending Fees: Total outstanding balances
   - Total Transactions: Number of payment records

2. **Student Payment Status Table**
   - All students listed with their payment status
   - Course fee (KES 4,000)
   - Amount paid
   - Balance remaining
   - Progress bar showing payment percentage
   - Quick "Pay" button for each student

3. **Recent Payments Table**
   - Last 10 payment transactions
   - Payment details (amount, date, method, reference)

### Payment Status Indicators

| Status | Indicator | Meaning |
|--------|-----------|---------|
| **Fully Paid** | Green "Paid" badge | Balance = KES 0 |
| **Partial Payment** | Red balance amount | Outstanding balance > 0 |
| **No Payment** | Red balance (KES 4,000) | No payments recorded |

### Progress Bars

Visual indication of payment progress:

- **Green (100%)**: Fully paid
- **Yellow (50-99%)**: Partially paid
- **Red (0-49%)**: Less than half paid

---

## How to Use

### View All Student Payments

1. Go to **Payments** (receptionist/admin only)
2. View **Student Payment Status** table
3. See each student's:
   - Name and cohort
   - Status (active/completed)
   - Course fee
   - Amount paid
   - Balance
   - Payment progress bar

### Record a Payment

1. Go to **Payments**
2. Find the student in the table
3. Click **"Pay"** button
4. Fill in payment details:
   - Amount
   - Payment method (cash/M-Pesa/bank/card)
   - Reference (optional)
   - Notes (optional)
5. Click **"Record Payment"**

### View Student Payment History

1. Go to **Payments**
2. Click **"Pay"** for any student
3. See full payment history at bottom of page
4. Each payment shows:
   - Amount
   - Date
   - Method
   - Reference
   - Notes

---

## Payment Methods

### Cash
- Physical cash payments
- Record immediately upon receipt
- Get receipt signed by student

### M-Pesa
- Mobile money transfer
- Record transaction code in Reference field
- Example: `QDH1234ABC`

### Bank Transfer
- Direct bank deposit
- Record bank reference number
- Example: `BNK12345678`

### Card Payment
- Credit/debit card payments
- Record last 4 digits of card
- Example: `Card ****1234`

---

## Payment Status Examples

### Example 1: Fully Paid Student

```
Student: John Doe
Course Fee: KES 4,000
Paid: KES 4,000
Balance: KES 0 (Green "Paid" badge)
Progress: 100% (Green bar)
```

### Example 2: Partial Payment

```
Student: Jane Smith
Course Fee: KES 4,000
Paid: KES 2,500
Balance: KES 1,500 (Red text)
Progress: 62.5% (Yellow bar)
```

### Example 3: No Payment

```
Student: Bob Wilson
Course Fee: KES 4,000
Paid: KES 0
Balance: KES 4,000 (Red text)
Progress: 0% (Red bar)
```

---

## Certificate Eligibility

**Important:** Students must pay the full course fee (KES 4,000) to be eligible for certificate generation.

The system automatically:
- Filters out students with balances from certificate generation
- Blocks certificate download if balance exists
- Shows balance warning when attempting to download certificate

---

## Reports

### Export Payment Data

1. Go to **Payments**
2. Click **"Export to Excel"**
3. Download includes:
   - All payment records
   - Student names
   - Amounts and dates
   - Payment methods
   - References

### Payment Summary

View key metrics at a glance:
- **Total Revenue**: Sum of all payments
- **Pending Fees**: Total outstanding balances
- **Total Transactions**: Count of payment records

---

## Best Practices

### For Receptionists

✅ **Do:**
- Record payments immediately upon receipt
- Always get transaction references for digital payments
- Provide receipts to students
- Verify payment amounts before recording
- Check student ID before recording

❌ **Don't:**
- Delay recording payments
- Record without proper reference
- Mix up student records
- Record incorrect amounts

### Payment Tracking

✅ **Daily:**
- Record all payments received that day
- Reconcile cash payments with physical cash
- Verify M-Pesa/bank payments with statements

✅ **Weekly:**
- Review outstanding balances
- Follow up on large balances
- Export payment report for backup

✅ **Monthly:**
- Generate payment reports
- Reconcile total revenue with bank statements
- Identify students with long-outstanding balances

---

## Troubleshooting

### Payment Not Showing

**Problem:** Payment recorded but not visible

**Solution:**
1. Refresh the page (F5)
2. Check if correct student was selected
3. Verify payment was saved (check success message)

### Incorrect Amount Recorded

**Problem:** Wrong amount entered

**Solution:**
1. Contact administrator
2. Cannot edit recorded payments
3. Admin may need to delete and re-record

### Student Shows Wrong Balance

**Problem:** Balance doesn't match expectations

**Solution:**
1. Click "Pay" to view payment history
2. Verify all payments are recorded
3. Check for duplicate payments
4. Contact administrator if issue persists

---

## Database Schema

### Payment Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| student_id | INTEGER | Foreign key → Student |
| amount | FLOAT | Payment amount |
| payment_date | DATETIME | When payment made |
| payment_method | VARCHAR | cash/mpesa/bank/card |
| reference | VARCHAR | Transaction reference |
| notes | TEXT | Additional notes |
| recorded_by | INTEGER | User who recorded |

### Relationships

- **Student**: One-to-many (one student → many payments)
- **User**: One-to-many (one user → many payments recorded)

---

## Security

### Access Control

- **Receptionist**: Can view and record payments
- **Admin**: Full access to all payment functions
- **Instructor**: Cannot access payments (restricted)

### Audit Trail

All payments record:
- Who recorded it (`recorded_by`)
- When it was recorded (`payment_date`)
- Original payment details (unchangeable)

---

## Support

For payment issues:
- Check this guide first
- Review payment history for the student
- Contact administrator for corrections

**Need Help?** Contact the system administrator.

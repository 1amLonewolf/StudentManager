# User Management & Role-Based Access Control

## 🎉 What's New!

Your StudentManager now has **complete user management** with **role-based access control**!

---

## 👥 User Roles

### 1. **Admin** (Full Access)
- ✅ All features available
- ✅ User management (add/edit/delete users)
- ✅ Students management
- ✅ Attendance tracking
- ✅ Assessments & certificates
- ✅ Payments & financial reports
- ✅ Messaging (Email + WhatsApp)
- ✅ System settings

### 2. **Instructor** (Teaching Staff)
- ✅ Students management
- ✅ Attendance tracking
- ✅ Assessments & certificates
- ✅ Messaging (Email + WhatsApp)
- ✅ View reports
- ❌ No access to: Payments, User Management

### 3. **Receptionist** (Administrative Staff)
- ✅ Students management
- ✅ Payments & fee tracking
- ✅ Messaging (Email + WhatsApp)
- ✅ View reports
- ❌ No access to: Attendance, Assessments, User Management

---

## 🔐 Default Login Credentials

After running the setup, you have 3 users:

| Role | Username | Password | Access Level |
|------|----------|----------|--------------|
| **Admin** | `admin` | `admin123` | Full Access |
| **Instructor** | `instructor` | `instructor123` | Teaching Access |
| **Receptionist** | `receptionist` | `receptionist123` | Admin Access |

**⚠️ IMPORTANT:** Change these passwords after first login!

---

## 🚀 Setup Instructions

### Step 1: Run Database Update

```bash
cd C:\Users\ADMIN\Desktop\StudentManager
venv\Scripts\python update_schema.py
```

This will:
- Add new user fields to database
- Create default admin user
- Create sample instructor and receptionist for testing

### Step 2: Login as Admin

1. Go to http://localhost:5000
2. Login with: `admin` / `admin123`
3. You'll see "User Management" in sidebar

### Step 3: Add More Users

1. Click **User Management** in sidebar
2. Click **Add User** button
3. Fill in:
   - Username (unique)
   - Password (min 6 characters)
   - Role (Admin/Instructor/Receptionist)
   - Active status
4. Click **Save User**

---

## 📋 User Management Features

### Admin Can:

#### Add Users
- Create new user accounts
- Assign roles
- Set active/inactive status

#### Edit Users
- Change username
- Reset passwords
- Change roles
- Activate/deactivate accounts

#### Delete Users
- Deactivate users (soft delete)
- Cannot delete own account

#### Reset Passwords
- Generate temporary passwords
- Force password change on next login

---

## 🔒 Access Control

### Sidebar Navigation

The sidebar **automatically shows/hides** menu items based on your role:

**Admin sees:**
- Dashboard
- Students
- Attendance
- Assessments
- Certificates
- Payments
- Messaging
- Reports
- **User Management** ← Admin only
- My Profile
- Logout

**Instructor sees:**
- Dashboard
- Students
- **Attendance** ✓
- **Assessments** ✓
- Certificates
- Messaging
- Reports
- My Profile
- Logout

**Receptionist sees:**
- Dashboard
- Students
- Certificates
- **Payments** ✓
- Messaging
- Reports
- My Profile
- Logout

---

## 👤 My Profile

Every user can:
- View their profile information
- See their role and permissions
- Change their password

**To access:** Click **My Profile** in sidebar (above Logout)

---

## 🔐 Password Management

### Change Your Password

1. Go to **My Profile**
2. Enter current password
3. Enter new password (min 6 characters)
4. Click **Change Password**

### Admin Reset User Password

1. Go to **User Management**
2. Click key icon 🔑 next to user
3. Temporary password generated
4. User must change on next login

---

## 📊 Role Permissions Matrix

| Feature | Admin | Instructor | Receptionist |
|---------|-------|------------|--------------|
| Dashboard | ✅ | ✅ | ✅ |
| Students (View/Add/Edit) | ✅ | ✅ | ✅ |
| Attendance | ✅ | ✅ | ❌ |
| Assessments | ✅ | ✅ | ❌ |
| Certificates | ✅ | ✅ | ✅ |
| Payments | ✅ | ❌ | ✅ |
| Messaging | ✅ | ✅ | ✅ |
| Reports | ✅ | ✅ | ✅ |
| **User Management** | ✅ | ❌ | ❌ |
| **Settings** | ✅ | ❌ | ❌ |

---

## 🛡️ Security Features

### Password Requirements
- Minimum 6 characters
- Stored as secure hash (not plain text)
- Password strength enforced

### Account Status
- Active/Inactive toggle
- Inactive users cannot login
- Soft delete (accounts not removed, just deactivated)

### Session Management
- Secure session cookies
- Auto-logout on browser close
- Login required for all pages

---

## 🎯 Best Practices

### For Admins:
1. ✅ Change default passwords immediately
2. ✅ Create individual accounts for each staff member
3. ✅ Assign appropriate roles based on job function
4. ✅ Deactivate (don't delete) accounts when staff leave
5. ✅ Review user list regularly

### For Instructors:
1. ✅ Manage student attendance daily
2. ✅ Record assessments promptly
3. ✅ Generate certificates for completed students
4. ✅ Use messaging for student communication

### For Receptionists:
1. ✅ Track all payments accurately
2. ✅ Send payment receipts via email
3. ✅ Monitor pending fees
4. ✅ Use messaging for payment reminders

---

## 🔧 Troubleshooting

### User Cannot Login

**Check:**
1. Account is Active (green status)
2. Username/password correct
3. No extra spaces in username

**Fix:**
- Admin can reset password from User Management

### Cannot See Menu Items

**Normal behavior** - menu items are role-based:
- Instructors see Attendance & Assessments
- Receptionists see Payments
- Only Admins see User Management

**Fix:**
- Admin can change user role in User Management

### Forgot Admin Password

**Recovery:**
1. Login with sample instructor account
2. Go to User Management
3. Reset admin password
4. Login as admin with new password

---

## 📝 Adding Custom Roles

Want to add more roles? Edit `models.py`:

```python
@property
def is_custom_role(self):
    return self.role in ['admin', 'custom_role_name']
```

Then use decorator in routes:
```python
@custom_role_required
def my_function():
    pass
```

---

## 🎓 Quick Start Guide

### First Time Setup:

```bash
# 1. Update database
venv\Scripts\python update_schema.py

# 2. Start app
run.bat

# 3. Login as admin
Username: admin
Password: admin123

# 4. Change admin password
Go to: My Profile → Change Password

# 5. Add staff accounts
Go to: User Management → Add User
```

### Daily Use:

1. **Login** with your credentials
2. **Access** your permitted features
3. **Logout** when done

---

## 📞 Support

For issues or questions:
- Check User Management page
- Contact system administrator
- Review this documentation

---

**Built with ❤️ for secure, role-based access control!**

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, FloatField, DateField, DateTimeField, SelectField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class StudentForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    id_number = StringField('ID Number', validators=[Optional(), Length(max=50)])
    gender = SelectField('Gender', choices=[('', 'Select'), ('Male', 'Male'), ('Female', 'Female')])
    cohort = StringField('Cohort (e.g., Jan-Mar 2026)', validators=[DataRequired(), Length(max=50)])
    course_id = SelectField('Course', coerce=int, validators=[Optional()])
    status = SelectField('Status', choices=[('active', 'Active'), ('completed', 'Completed'), ('dropped', 'Dropped')], default='active')
    submit = SubmitField('Save Student')

class AttendanceForm(FlaskForm):
    student_id = IntegerField('Student ID', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    module = SelectField('Module', choices=[
        ('Word', 'MS Word'),
        ('Excel', 'MS Excel'),
        ('PowerPoint', 'MS PowerPoint'),
        ('Access', 'MS Access'),
        ('Internet', 'Internet Basics')
    ])
    present = BooleanField('Present')
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save Attendance')

class AssessmentForm(FlaskForm):
    student_id = IntegerField('Student ID', validators=[DataRequired()])
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])
    module = SelectField('Module', choices=[
        ('Word', 'MS Word'),
        ('Excel', 'MS Excel'),
        ('PowerPoint', 'MS PowerPoint'),
        ('Access', 'MS Access'),
        ('Internet', 'Internet Basics')
    ], validators=[DataRequired()])
    score = IntegerField('Score', validators=[DataRequired(), NumberRange(min=0, max=100)])
    max_score = IntegerField('Max Score', default=100, validators=[DataRequired(), NumberRange(min=1)])
    assessment_type = SelectField('Assessment Type', choices=[
        ('practical', 'Practical'),
        ('theory', 'Theory'),
        ('final', 'Final Exam')
    ], default='practical')
    remarks = TextAreaField('Remarks', validators=[Optional()])
    submit = SubmitField('Save Assessment')

class PaymentForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    payment_method = SelectField('Payment Method', choices=[
        ('cash', 'Cash'),
        ('mpesa', 'M-Pesa'),
        ('bank', 'Bank Transfer'),
        ('card', 'Card')
    ], validators=[DataRequired()])
    reference = StringField('Reference/Transaction ID', validators=[Optional(), Length(max=100)])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Record Payment')

class CertificateForm(FlaskForm):
    student_id = IntegerField('Student ID', validators=[DataRequired()])
    course_name = StringField('Course Name', validators=[DataRequired(), Length(max=100)])
    modules_completed = TextAreaField('Modules Completed', validators=[DataRequired()])
    grade = SelectField('Grade', choices=[
        ('Pass', 'Pass'),
        ('Credit', 'Credit'),
        ('Distinction', 'Distinction')
    ], validators=[DataRequired()])
    submit = SubmitField('Generate Certificate')

class SMSForm(FlaskForm):
    recipients = StringField('Recipients (phone numbers, comma-separated)', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=1600)])
    submit = SubmitField('Send SMS')

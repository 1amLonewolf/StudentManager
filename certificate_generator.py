"""
Certificate Generator
Generates PDF certificates by overlaying student data on template
"""
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image

def generate_certificate(student, certificate_number, modules_completed, grade, template_path=None):
    """
    Generate a certificate PDF for a student

    Args:
        student: Student object
        certificate_number: Unique certificate number
        modules_completed: List of module names
        grade: Pass/Credit/Distinction
        template_path: Path to certificate template image (optional)

    Returns:
        Path to generated PDF
    """
    from flask import current_app

    # Get template path from config or use default
    if template_path is None:
        template_path = current_app.config.get('CERTIFICATE_TEMPLATE_PATH')

    output_dir = current_app.config.get('OUTPUT_CERTIFICATE_PATH', 'static/certificates/generated')
    os.makedirs(output_dir, exist_ok=True)

    # Generate output filename
    filename = f"Colmac_Computer_College_Certificate_{certificate_number}.pdf"
    output_path = os.path.join(output_dir, filename)

    # Create PDF with A4 portrait orientation
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4  # 595 x 842 points

    # Check if template exists
    template_exists = template_path and os.path.exists(template_path)

    if template_exists:
        # Use the custom template as background
        c.drawImage(template_path, 0, 0, width=width, height=height)
        
        # Add student name on the blank line under "This is to certify that"
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(colors.black)
        c.drawCentredString(width / 2, height * 0.62, student.name)
        
        # Add training period dates (from/to on the dotted lines)
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.black)
        start_date = student.enrollment_date.strftime("%d %B %Y") if student.enrollment_date else "_______________"
        completion_date = datetime.now().strftime("%d %B %Y")
        c.drawString(width * 0.15, height * 0.56, start_date)
        c.drawString(width * 0.35, height * 0.56, completion_date)
        
        # Add modules list (already printed on template, this is for reference)
        # Modules are pre-printed on the template
        
        # Add issue date on the "on this day of" line
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.black)
        issue_date = datetime.now().strftime("%d %B %Y")
        c.drawString(width * 0.32, height * 0.29, issue_date)
        
        # Add overall grade next to "Overall Grade:"
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.darkblue)
        c.drawString(width * 0.20, height * 0.19, grade)
        
        # Add signature lines (for manual signing - Trainer and Director)
        # Signatures are pre-printed on template
        
        # Add certificate number at bottom (optional, can be removed if not needed)
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.grey)
        c.drawCentredString(width / 2, height * 0.05, f"Certificate No: {certificate_number}")
        
    else:
        # Create a simple certificate design (fallback)
        draw_basic_certificate(c, width, height, certificate_number, student)

    c.save()

    return output_path


def draw_basic_certificate(c, width, height, certificate_number, student):
    """Draw a basic certificate design when no template is provided"""

    # Border
    c.setStrokeColor(colors.darkblue)
    c.setLineWidth(5)
    c.rect(0.5 * inch, 0.5 * inch, width - 1 * inch, height - 1 * inch)

    # Inner border
    c.setStrokeColor(colors.gold)
    c.setLineWidth(2)
    c.rect(0.7 * inch, 0.7 * inch, width - 1.4 * inch, height - 1.4 * inch)

    # Title
    c.setFont("Helvetica-Bold", 48)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(width / 2, height - 2 * inch, "CERTIFICATE")
    c.drawCentredString(width / 2, height - 2.5 * inch, "OF COMPLETION")

    # Subtitle
    c.setFont("Helvetica", 16)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, height - 3.2 * inch, "This is to certify that")

    # Student name
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, height * 0.62, student.name)

    # Decorative elements
    c.setFillColor(colors.gold)
    c.circle(1.5 * inch, height - 2 * inch, 0.3 * inch, fill=1)
    c.circle(width - 1.5 * inch, height - 2 * inch, 0.3 * inch, fill=1)
    c.circle(1.5 * inch, 2 * inch, 0.3 * inch, fill=1)
    c.circle(width - 1.5 * inch, 2 * inch, 0.3 * inch, fill=1)


def generate_certificate_preview(student, modules_completed):
    """
    Generate certificate data for preview (without creating PDF)
    Used for displaying certificate info before generation
    """
    return {
        'student_name': student.name,
        'course_name': 'Computer Packages',
        'modules_completed': modules_completed,
        'completion_date': datetime.now().strftime("%d %B %Y"),
        'grade': 'Pass' if student.average_score >= 50 else 'Pass'
    }

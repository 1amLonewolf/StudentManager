"""
Certificate Generator
Generates PDF certificates by overlaying student data on a template
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
    
    # Create PDF (portrait orientation to match template)
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    # Check if template exists
    template_exists = template_path and os.path.exists(template_path)

    if template_exists:
        # Use template as background (logo already included in template)
        c.drawImage(template_path, 0, 0, width=width, height=height)
    else:
        # Create a simple certificate design
        draw_basic_certificate(c, width, height, certificate_number)

    # Add student name (centered) - on the blank line under "This is to certify that"
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, height * 0.58, student.name)

    # Add training period (from/to dates on the dotted lines)
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.black)
    start_date = student.enrollment_date.strftime("%d %B %Y") if student.enrollment_date else "____________"
    completion_date = datetime.now().strftime("%d %B %Y")
    c.drawCentredString(width * 0.30, height * 0.52, start_date)
    c.drawCentredString(width * 0.60, height * 0.52, completion_date)

    # Add grade - next to "Overall Grade:" label
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.darkblue)
    c.drawString(width * 0.22, height * 0.16, grade)

    # Add issue date on the "on this day of" line
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, height * 0.23, completion_date)

    # Add certificate number at bottom center
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, height * 0.06, f"Certificate No: {certificate_number}")

    # Add signature lines (for manual signing - Trainer and Director)
    c.setLineWidth(1)
    c.line(width * 0.15, height * 0.11, width * 0.38, height * 0.11)
    c.line(width * 0.62, height * 0.11, width * 0.85, height * 0.11)
    
    c.save()
    
    return output_path


def draw_basic_certificate(c, width, height, certificate_number):
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

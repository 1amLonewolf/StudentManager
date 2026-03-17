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
    filename = f"certificate_{certificate_number}.pdf"
    output_path = os.path.join(output_dir, filename)
    
    # Create PDF
    c = canvas.Canvas(output_path, pagesize=landscape(A4))
    width, height = landscape(A4)
    
    # Check if template exists
    template_exists = template_path and os.path.exists(template_path)
    
    if template_exists:
        # Use template as background
        c.drawImage(template_path, 0, 0, width=width, height=height)
    else:
        # Create a simple certificate design
        draw_basic_certificate(c, width, height, certificate_number)
    
    # Add student name (centered)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(width / 2, height / 2 + 0.5 * inch, student.name)
    
    # Add course name
    c.setFont("Helvetica", 18)
    c.drawCentredString(width / 2, height / 2 - 0.3 * inch, "Computer Packages Course")
    
    # Add completion date
    completion_date = datetime.now().strftime("%d %B %Y")
    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height / 2 - 0.8 * inch, f"Completed on {completion_date}")
    
    # Add modules completed
    modules_text = ", ".join(modules_completed) if modules_completed else "Word, Excel, PowerPoint, Access, Internet"
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height / 2 - 1.2 * inch, f"Modules: {modules_text}")
    
    # Add grade
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height / 2 - 1.6 * inch, f"Grade: {grade}")
    
    # Add certificate number
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, 1 * inch, f"Certificate No: {certificate_number}")
    
    # Add issue date
    c.drawCentredString(width / 2, 0.7 * inch, f"Issued: {datetime.now().strftime('%d/%m/%Y')}")
    
    # Add signature line
    c.line(2 * inch, 1.5 * inch, 4 * inch, 1.5 * inch)
    c.drawCentredString(3 * inch, 1.3 * inch, "Course Instructor")
    
    c.line(width - 4 * inch, 1.5 * inch, width - 2 * inch, 1.5 * inch)
    c.drawCentredString(width - 3 * inch, 1.3 * inch, "College Administrator")
    
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

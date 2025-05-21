from flask import Flask, request, render_template, redirect, url_for, send_file
import os
from werkzeug.utils import secure_filename
from resume_parser import parse_resume
from job_matcher import match_jobs
import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'resumes'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_pdf(profile):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    story.append(Paragraph(profile['name'], title_style))
    story.append(Spacer(1, 0.1 * inch))

    # Contact Information
    contact_style = ParagraphStyle(
        'Contact',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=20
    )
    contact_info = f"{profile['email']} | {profile['phone']}"
    story.append(Paragraph(contact_info, contact_style))
    story.append(Spacer(1, 0.2 * inch))

    # Education
    story.append(Paragraph("Education", styles['Heading2']))
    story.append(Spacer(1, 0.1 * inch))
    for edu in profile['education']:
        story.append(Paragraph(edu, styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # Experience
    story.append(Paragraph("Experience", styles['Heading2']))
    story.append(Spacer(1, 0.1 * inch))
    for exp in profile['experience']:
        story.append(Paragraph(exp, styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # Skills
    story.append(Paragraph("Skills", styles['Heading2']))
    story.append(Spacer(1, 0.1 * inch))
    
    # Create a table for skills
    skills_data = [[Paragraph(skill, styles['Normal'])] for skill in profile['skills']]
    skills_table = Table(skills_data, colWidths=[4 * inch])
    skills_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(skills_table)

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'resume' not in request.files:
            return 'No file uploaded', 400
        
        file = request.files['resume']
        if file.filename == '':
            return 'No file selected', 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Parse resume and match jobs
            profile = parse_resume(filepath)
            jobs, scores, gaps = match_jobs(profile)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return render_template('results.html', profile=profile, jobs=jobs, scores=scores, gaps=gaps)
    
    return render_template('index.html')

@app.route('/create-resume', methods=['POST'])
def create_resume():
    # Get form data
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    education = request.form.get('education')
    experience = request.form.get('experience')
    skills = request.form.get('skills', '').split(',')
    
    # Create profile dictionary
    profile = {
        'name': name,
        'email': email,
        'phone': phone,
        'education': [edu.strip() for edu in education.split('\n') if edu.strip()],
        'experience': [exp.strip() for exp in experience.split('\n') if exp.strip()],
        'skills': [skill.strip() for skill in skills if skill.strip()]
    }
    
    # Check if it's a PDF download request
    if request.headers.get('Accept') == 'application/pdf':
        pdf_buffer = generate_pdf(profile)
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='resume.pdf'
        )
    
    # Match jobs with the created profile
    jobs, scores, gaps = match_jobs(profile)
    
    return render_template('results.html', profile=profile, jobs=jobs, scores=scores, gaps=gaps)

if __name__ == '__main__':
    app.run(debug=True) 
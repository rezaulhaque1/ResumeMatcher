import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import docx
import PyPDF2

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

SKILL_SET = set(['python', 'java', 'c++', 'machine learning', 'data analysis', 'sql', 'excel', 'communication', 'project management'])

EMAIL_REGEX = r'[\w\.-]+@[\w\.-]+'  # simple email regex
PHONE_REGEX = r'\+?\d[\d\s\-]{8,}\d'

def extract_text_from_pdf(filepath):
    text = ''
    with open(filepath, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + '\n'
    return text

def extract_text_from_docx(filepath):
    doc = docx.Document(filepath)
    return '\n'.join([para.text for para in doc.paragraphs])

def extract_contact_info(text):
    email = re.findall(EMAIL_REGEX, text)
    phone = re.findall(PHONE_REGEX, text)
    return (email[0] if email else None, phone[0] if phone else None)

def extract_name(text):
    # Simple name extraction using regex
    # Look for common name patterns
    name_pattern = r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*'
    lines = text.split('\n')
    for line in lines:
        if re.match(name_pattern, line.strip()):
            return line.strip()
    return None

def extract_skills(text):
    text_lower = text.lower()
    found = [skill for skill in SKILL_SET if skill in text_lower]
    return found

def extract_education(text):
    education_keywords = ['bachelor', 'master', 'phd', 'b.sc', 'm.sc', 'b.tech', 'm.tech', 'mba']
    lines = text.lower().split('\n')
    edu = [line for line in lines if any(k in line for k in education_keywords)]
    return edu

def extract_experience(text):
    # Simple heuristic: look for years or durations
    exp_regex = r'(\d+\+? years|\d+ years|\d+ months)'
    matches = re.findall(exp_regex, text.lower())
    return matches

def parse_resume(filepath):
    if filepath.endswith('.pdf'):
        text = extract_text_from_pdf(filepath)
    elif filepath.endswith('.docx'):
        text = extract_text_from_docx(filepath)
    else:
        raise ValueError('Unsupported file type')
    name = extract_name(text)
    email, phone = extract_contact_info(text)
    skills = extract_skills(text)
    education = extract_education(text)
    experience = extract_experience(text)
    return {
        'name': name,
        'email': email,
        'phone': phone,
        'skills': skills,
        'education': education,
        'experience': experience
    } 
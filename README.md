# AI-Powered Resume Analyzer & Job Matcher

An intelligent web application that analyzes resumes, matches them with job listings, and helps create professional resumes using AI.

## Features

- 📄 Resume Analysis
  - Extract key information from resumes (PDF/DOCX)
  - Identify skills, experience, and education
  - Smart text extraction and parsing

- 🤖 AI-Powered Job Matching
  - Match resume with relevant job listings
  - Calculate match percentage
  - Identify missing skills
  - Visual match analysis

- ✨ Resume Builder
  - Create professional resumes
  - Live preview
  - PDF download
  - AI-powered suggestions

- 📊 Interactive Dashboard
  - Visual job match distribution
  - Skills analysis
  - Match percentage charts
  - Missing skills visualization

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ResumeMatcher.git
cd ResumeMatcher
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix/MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and visit:
```
http://localhost:5000
```

## Requirements

- Python 3.7+
- Flask
- pandas
- python-docx
- PyPDF2
- fuzzywuzzy
- nltk
- reportlab

## Project Structure

```
ResumeMatcher/
├── app.py              # Main Flask application
├── resume_parser.py    # Resume parsing logic
├── job_matcher.py      # Job matching algorithm
├── templates/          # HTML templates
│   ├── index.html     # Main page
│   └── results.html   # Results page
├── static/            # Static files
│   ├── css/          # Stylesheets
│   └── js/           # JavaScript files
└── resumes/          # Uploaded resumes storage
```

## Usage

1. **Analyze Resume**
   - Upload your resume (PDF/DOCX)
   - Get instant analysis
   - View job matches
   - See missing skills

2. **Create Resume**
   - Fill in your details
   - Get AI suggestions
   - Preview your resume
   - Download as PDF

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Flask for the web framework
- NLTK for natural language processing
- ReportLab for PDF generation
- All contributors and users of this project 
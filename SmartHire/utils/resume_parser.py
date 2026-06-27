import re
import io

# ---- Skills Database ----
ALL_SKILLS = {
    'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'typescript', 'go', 'rust',
                    'kotlin', 'swift', 'r', 'scala', 'php', 'ruby', 'dart', 'c'],
    'web': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django',
            'flask', 'fastapi', 'next.js', 'bootstrap', 'tailwind', 'graphql', 'rest api'],
    'data': ['pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly', 'tableau', 'power bi',
             'excel', 'sql', 'postgresql', 'mysql', 'mongodb', 'data analysis'],
    'ml': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras', 'scikit-learn',
           'nlp', 'computer vision', 'transformers', 'bert', 'opencv', 'xgboost', 'neural network'],
    'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'ci/cd', 'linux',
              'devops', 'git', 'github', 'jenkins', 'ansible'],
    'soft': ['leadership', 'communication', 'teamwork', 'problem solving', 'agile', 'scrum',
             'project management', 'analytical', 'critical thinking'],
}

FLAT_SKILLS = [s for skills in ALL_SKILLS.values() for s in skills]

def parse_pdf(file_bytes):
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
        return text.strip()
    except Exception as e:
        return f"[Could not parse PDF: {e}]"

def parse_docx(file_bytes):
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_bytes))
        text = '\n'.join(para.text for para in doc.paragraphs)
        return text.strip()
    except Exception as e:
        return f"[Could not parse DOCX: {e}]"

def parse_resume(uploaded_file):
    """Return extracted text from uploaded resume."""
    name = uploaded_file.name.lower()
    file_bytes = uploaded_file.read()
    if name.endswith('.pdf'):
        return parse_pdf(file_bytes)
    elif name.endswith('.docx') or name.endswith('.doc'):
        return parse_docx(file_bytes)
    else:
        # Plain text
        try:
            return file_bytes.decode('utf-8')
        except Exception:
            return file_bytes.decode('latin-1', errors='replace')

def extract_skills(text: str):
    text_lower = text.lower()
    found = []
    for skill in FLAT_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found.append(skill.title())
    return list(dict.fromkeys(found))  # deduplicate preserving order

def extract_email(text: str):
    match = re.search(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', text)
    return match.group(0) if match else ''

def extract_phone(text: str):
    match = re.search(r'(\+?\d[\d\s\-]{8,}\d)', text)
    return match.group(0).strip() if match else ''

def extract_education(text: str):
    edu_keywords = ['b.tech', 'b.e', 'bsc', 'bca', 'mca', 'm.tech', 'msc', 'phd',
                    'bachelor', 'master', 'engineering', 'computer science', 'information technology',
                    'b.com', 'bba', 'mba', 'diploma']
    lines = text.split('\n')
    edu = []
    for line in lines:
        if any(kw in line.lower() for kw in edu_keywords):
            clean = line.strip()
            if len(clean) > 5:
                edu.append(clean)
    return edu[:4]

def extract_experience(text: str):
    exp_keywords = ['intern', 'developer', 'engineer', 'analyst', 'manager', 'consultant',
                    'researcher', 'trainer', 'freelancer', 'associate']
    lines = text.split('\n')
    exp = []
    for line in lines:
        if any(kw in line.lower() for kw in exp_keywords):
            clean = line.strip()
            if len(clean) > 10:
                exp.append(clean)
    return exp[:5]

def compute_resume_score(skills, education, experience, text):
    score = 0
    score += min(len(skills) * 4, 40)     # up to 40 pts for skills
    score += min(len(education) * 10, 20)  # up to 20 pts for education
    score += min(len(experience) * 6, 24)  # up to 24 pts for experience
    if len(text) > 500: score += 8         # content length
    if extract_email(text): score += 4     # contact info
    if extract_phone(text): score += 4     # phone
    return min(score, 100)

# analyzer/utils.py
import re
from io import BytesIO
from pathlib import Path

from PyPDF2 import PdfReader
import docx

# Helper to extract text
def extract_text_from_file(fpath):
    fpath = Path(fpath)
    ext = fpath.suffix.lower()
    text = ""
    try:
        if ext == '.pdf':
            reader = PdfReader(str(fpath))
            parts = []
            for page in reader.pages:
                page_text = page.extract_text() or ""
                parts.append(page_text)
            text = "\n".join(parts)
        elif ext in ['.docx', '.doc']:
            # docx
            doc = docx.Document(str(fpath))
            parts = [p.text for p in doc.paragraphs]
            text = "\n".join(parts)
        else:
            # try reading as text file
            text = fpath.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        # best-effort extraction
        text += f"\n\n[Extraction error: {e}]"
    return text

# Basic patterns
SECTION_KEYWORDS = {
    'experience': ['experience', 'work experience', 'professional experience', 'employment history', 'projects'],
    'education': ['education', 'academic', 'qualifications'],
    'skills': ['skills', 'technical skills', 'key skills'],
    'summary': ['summary', 'objective', 'profile'],
    'contact': ['phone', 'email', 'contact', 'linkedin', 'github']
}

SAMPLE_SKILLS = ['python','django','sql','javascript','react','aws','git','excel','pandas','numpy','tensorflow','machine learning']

def contains_any(text, keywords):
    t = text.lower()
    return any(k in t for k in keywords)

def simple_ats_score(text):
    """
    Return (score:int, checks:dict)
    checks shows which elements were found for feedback.
    """
    checks = {}
    t = text.lower()

    # length
    words = re.findall(r'\w+', t)
    word_count = len(words)
    checks['word_count'] = word_count

    # check sections
    for key, kws in SECTION_KEYWORDS.items():
        checks[f'has_{key}'] = contains_any(t, kws)

    # check contact info
    email_found = re.search(r'[\w\.-]+@[\w\.-]+', t) is not None
    phone_found = re.search(r'(\+?\d{7,15})', t) is not None  # loose phone detection
    checks['has_email'] = email_found
    checks['has_phone'] = phone_found

    # skill matches
    skills_found = [s for s in SAMPLE_SKILLS if s in t]
    checks['skills_found'] = skills_found
    checks['num_skills_found'] = len(skills_found)

    # scoring logic (simple, rule-based)
    score = 0

    # base points for sections
    score += 15 if checks['has_experience'] else 0
    score += 10 if checks['has_education'] else 0
    score += 10 if checks['has_skills'] else 0
    score += 10 if checks['has_summary'] else 0

    # contact
    score += 10 if email_found else 0
    score += 5 if phone_found else 0

    # skills richness
    score += min(15, checks['num_skills_found'] * 3 + (5 if checks['num_skills_found']>0 else 0))

    # length: good if 200-1000 words (resume too short or extremely long penalized)
    if 200 <= word_count <= 1000:
        score += 15
    elif word_count >= 1000:
        score += 8
    elif word_count < 200:
        score += 5

    # final normalization
    if score > 100:
        score = 100

    # Determine ATS-friendly: simple rule — must have contact, skills, and experience
    ats_friendly = email_found and checks['has_skills'] and checks['has_experience']

    return int(score), checks, ats_friendly

def generate_feedback(checks, score):
    tips = []
    t = checks
    if not t.get('has_experience'):
        tips.append("Add a clear 'Experience' or 'Work Experience' section with role, company, dates and 2-4 bullet points each.")
    else:
        tips.append("Format experience entries with bullet points focusing on achievements and quantifiable impact.")

    if not t.get('has_education'):
        tips.append("Include an 'Education' section with degree, institution and graduation year.")
    if not t.get('has_skills'):
        tips.append("Add a 'Skills' section listing relevant technical skills (comma or bullet list).")
    else:
        if t.get('num_skills_found',0) < 3:
            tips.append("Include more relevant skills (aim for 6-12). Use exact technology names (e.g., 'Django', 'SQL').")

    if not t.get('has_email'):
        tips.append("Add a professional email address (e.g., yourname@example.com).")
    if not t.get('has_phone'):
        tips.append("Add a phone number for contact.")

    wc = t.get('word_count',0)
    if wc < 180:
        tips.append("Resume looks short — expand with more details on projects/impact (aim 200–800 words).")
    elif wc > 1200:
        tips.append("Resume is very long — keep it concise by focusing on recent and relevant experience (1–2 pages).")

    # general tips based on score
    if score >= 85:
        tips.append("Great — the resume looks well-structured for ATS. Keep formatting simple: plain fonts, no images.")
    elif score >= 60:
        tips.append("Good start — refine formatting and add more keywords from job descriptions you target.")
    else:
        tips.append("Consider optimizing headings, adding keywords, and simplifying layout for ATS (remove tables/graphics).")

    return "\n".join(tips)

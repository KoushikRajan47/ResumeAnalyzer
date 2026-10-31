# analyzer/views.py
import re
from django.shortcuts import render
from .forms import ResumeUploadForm
from PyPDF2 import PdfReader
import docx

SAMPLE_DEMO_RESUME = """
Alex Mercer
Senior Software Engineer | Cloud & Full-Stack Architect
Email: alex.mercer@example.com | Phone: +1 (555) 234-5678 | San Francisco, CA
LinkedIn: linkedin.com/in/alex-mercer | GitHub: github.com/alex-mercer

PROFESSIONAL SUMMARY
Dynamic and results-driven Senior Software Engineer with over 6 years of experience building scalable, high-concurrency web platforms and microservices. Expert in Python, Django, React, AWS cloud architecture, and PostgreSQL. Proven track record of improving system uptime by 35% and reducing API latency by 40%.

SKILLS & TECHNOLOGIES
Languages & Frameworks: Python, Django, Flask, JavaScript, TypeScript, React, SQL, HTML/CSS
Cloud & DevOps: AWS (EC2, S3, RDS, Lambda), Docker, Kubernetes, CI/CD, Git, Linux
Databases & Tools: PostgreSQL, MySQL, Redis, REST APIs, GraphQL, Agile/Scrum

WORK EXPERIENCE
Senior Full-Stack Engineer | CloudPeak Systems | 2021 - Present
- Architected high-performance Django REST microservices serving over 2.5 million daily active users with 99.99% availability.
- Led migration from monolithic architecture to AWS ECS Docker containers, cutting operational costs by 28%.
- Optimized complex PostgreSQL database queries and implemented Redis caching, reducing page load times from 2.1s to 450ms.
- Mentored a distributed team of 8 junior and mid-level software engineers through code reviews and agile sprints.

Software Engineer | Apex Digital Solutions | 2018 - 2021
- Developed scalable web applications using Python, Django, React, and Redux.
- Built automated CI/CD deployment pipelines using GitHub Actions, reducing deployment errors by 65%.
- Integrated third-party payment gateways (Stripe, PayPal) handling $15M+ annual processing volume securely.

EDUCATION
Bachelor of Science in Computer Science | University of California, Berkeley | 2014 - 2018
- GPA: 3.8 / 4.0, Dean's Honor List

KEY PROJECTS
- CloudFlow Engine: Open-source distributed task queue built with Python, Redis, and WebSockets (1.2k GitHub Stars).
- ATS Resume Optimizer: Machine learning web app for automatic keyword analysis and candidate score modeling using Django and PyPDF2.
"""

TECH_KEYWORDS = [
    'python', 'django', 'sql', 'react', 'javascript', 'typescript', 'aws',
    'docker', 'kubernetes', 'postgresql', 'mysql', 'git', 'ci/cd', 'rest api',
    'machine learning', 'redis', 'flask', 'linux', 'html', 'css', 'agile'
]


def home(request):
    """
    Landing page showcasing platform capabilities and ATS metrics.
    """
    return render(request, 'analyzer/home.html')


def _extract_text_from_file(uploaded_file):
    """
    Extract text content safely from PDF or DOCX file.
    """
    name = uploaded_file.name.lower()
    text = ""
    try:
        if name.endswith('.pdf'):
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                ptext = page.extract_text()
                if ptext:
                    text += ptext + "\n"
        elif name.endswith('.docx'):
            doc = docx.Document(uploaded_file)
            for p in doc.paragraphs:
                if p.text:
                    text += p.text + "\n"
        else:
            return ""
    except Exception as exc:
        print(f"Extraction error: {exc}")
        return ""
    return text


def upload_resume(request):
    """
    Handle resume uploads and demo evaluation, computing ATS metrics,
    section checks, keyword density, and actionable advice.
    """
    form = ResumeUploadForm(request.POST or None, request.FILES or None)
    context = {
        'form': form,
        'ats_score': None,
        'feedback': None,
        'tips': [],
        'sections_status': {},
        'contact_info': {},
        'found_keywords': [],
        'missing_keywords': [],
        'word_count': 0,
        'file_name': None,
        'extracted_snippet': '',
        'verdict_badge': '',
        'verdict_class': '',
        'gauge_offset': 471,
    }

    # Support 1-click Demo Resume evaluation
    is_demo = request.GET.get('demo') == '1' or request.POST.get('demo') == '1'

    if is_demo:
        text = SAMPLE_DEMO_RESUME.strip()
        context['file_name'] = "Alex_Mercer_Senior_Software_Engineer.pdf (Demo Resume)"
    elif request.method == 'POST':
        if not form.is_valid():
            context['feedback'] = "Invalid upload. Please select a valid .pdf or .docx resume file."
            return render(request, 'analyzer/upload.html', context)

        uploaded = request.FILES.get('file')
        if not uploaded:
            context['feedback'] = "No file received. Please choose a file to analyze."
            return render(request, 'analyzer/upload.html', context)

        context['file_name'] = uploaded.name
        text = _extract_text_from_file(uploaded)
    else:
        return render(request, 'analyzer/upload.html', context)

    # Validate extracted text
    if not text.strip():
        context['feedback'] = "Could not extract text. Please ensure the document is a text-based PDF or DOCX (not an image scan)."
        context['ats_score'] = 40
        context['verdict_badge'] = "Unreadable Scan"
        context['verdict_class'] = "badge-warning"
        context['tips'] = [
            "Use standard selectable text rather than an image scan of your resume.",
            "Save your document directly as PDF from Microsoft Word, Google Docs, or LaTeX.",
            "Verify that key section headings (Experience, Education, Skills) are clearly written in standard text."
        ]
        context['gauge_offset'] = int(471 - (40 / 100.0) * 471)
        return render(request, 'analyzer/upload.html', context)

    low = text.lower()
    words = re.findall(r'\b[a-zA-Z0-9_\-\.\+]+\b', low)
    word_count = len(words)
    context['word_count'] = word_count
    context['extracted_snippet'] = text[:1500] + ("..." if len(text) > 1500 else "")

    # Section Detection
    has_experience = any(k in low for k in ['experience', 'work experience', 'employment', 'career history'])
    has_education = any(k in low for k in ['education', 'academic', 'university', 'degree', 'bachelor', 'master'])
    has_skills = any(k in low for k in ['skills', 'technologies', 'technical proficiency', 'core competencies'])
    has_projects = any(k in low for k in ['project', 'projects', 'portfolio', 'github'])
    has_summary = any(k in low for k in ['summary', 'profile', 'objective', 'about me'])

    context['sections_status'] = {
        'Experience': has_experience,
        'Education': has_education,
        'Skills': has_skills,
        'Projects': has_projects,
        'Summary': has_summary,
    }

    # Contact Info Detection
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}', text)
    has_linkedin = 'linkedin.com' in low
    has_github = 'github.com' in low or 'github' in low

    context['contact_info'] = {
        'email': email_match.group(0) if email_match else None,
        'phone': phone_match.group(0) if phone_match else None,
        'has_linkedin': has_linkedin,
        'has_github': has_github,
    }

    # Keyword Matching
    found_keywords = [kw for kw in TECH_KEYWORDS if re.search(r'\b' + re.escape(kw) + r'\b', low)]
    missing_keywords = [kw for kw in TECH_KEYWORDS if kw not in found_keywords][:8]
    context['found_keywords'] = found_keywords
    context['missing_keywords'] = missing_keywords

    # Algorithmic ATS Scoring
    score = 30  # Baseline

    # Section points (up to 35 pts)
    if has_experience: score += 12
    if has_education: score += 8
    if has_skills: score += 8
    if has_projects: score += 4
    if has_summary: score += 3

    # Contact points (up to 15 pts)
    if email_match: score += 8
    if phone_match: score += 4
    if has_linkedin or has_github: score += 3

    # Keyword density points (up to 25 pts)
    kw_score = min(25, len(found_keywords) * 3)
    score += kw_score

    # Word count calibration (up to 15 pts)
    if 300 <= word_count <= 950:
        score += 15
    elif 200 <= word_count < 300 or 950 < word_count <= 1400:
        score += 8
    elif word_count < 200:
        score -= 5
    elif word_count > 1600:
        score -= 5

    # Boundary clamp
    score = max(20, min(98, score))
    context['ats_score'] = int(score)

    # Offset for 471.24 circumference SVG circle (r=75)
    context['gauge_offset'] = int(471.24 - (score / 100.0) * 471.24)

    # Qualitative verdict
    if score >= 85:
        context['verdict_badge'] = "ATS Optimal — High Interview Likelihood"
        context['verdict_class'] = "badge-excellent"
        context['feedback'] = "Outstanding resume! Clean structure, strong keyword concentration, and comprehensive contact details align with modern ATS parsers."
    elif score >= 65:
        context['verdict_badge'] = "Good Foundation — Needs Targeted Refinements"
        context['verdict_class'] = "badge-good"
        context['feedback'] = "Solid profile with recognizable credentials. Adding quantified impact bullets and broadening targeted technical keywords will push this into top candidate tier."
    else:
        context['verdict_badge'] = "Needs Optimization — Missing Core Signals"
        context['verdict_class'] = "badge-warning"
        context['feedback'] = "Your resume is missing critical sections or keywords that automated ATS filters scan for before a human recruiter ever sees it."

    # Actionable Tips Generation
    tips = []
    if not has_experience:
        tips.append("Add a dedicated 'Work Experience' section with company names, official titles, employment dates, and bulleted deliverables.")
    if not has_education:
        tips.append("Include an 'Education' section highlighting your degree, institution, and graduation year.")
    if not has_skills or len(found_keywords) < 4:
        tips.append("Create an explicit 'Skills' section with comma-separated technical keywords matching the jobs you apply for (e.g., Python, SQL, AWS, React).")
    if not email_match:
        tips.append("Ensure your professional email address is formatted clearly in the header.")
    if not phone_match:
        tips.append("Include a readable telephone number with country/area code.")
    if not (has_linkedin or has_github):
        tips.append("Link your LinkedIn profile or GitHub/portfolio URL to provide social proof of your projects and experience.")
    if word_count < 280:
        tips.append("Your resume content is on the shorter side. Expand on project impact using the STAR method (Situation, Task, Action, Result).")
    elif word_count > 1100:
        tips.append("Your resume exceeds standard ATS brevity. Consider condensing into 1-2 tight, high-impact pages.")

    if not tips:
        tips.append("Keep your formatting clean and avoid nested tables, columns, or graphics that confuse older ATS parsers.")
        tips.append("Tailor keywords for each job posting to maintain a 90%+ match rate.")

    context['tips'] = tips

    return render(request, 'analyzer/upload.html', context)


def resume_builder(request):
    """
    Interactive full-featured Resume Builder with live preview,
    pre-fill demo data, and instant PDF print formatting.
    """
    return render(request, 'analyzer/builder.html', {})

# 📄 ResumeAI Studio — Modern ATS Resume Analyzer & Live Builder

[![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![CSS3](https://img.shields.io/badge/Vanilla_CSS3-Glassmorphism-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

> **ResumeAI Studio** is an intelligent, privacy-first web application designed to help job seekers beat automated Applicant Tracking Systems (ATS). Built with Django and Vanilla CSS glassmorphism, it provides instant algorithmic resume scoring, keyword gap diagnostics, structural format verification, and an interactive real-time resume builder with 1-click PDF export.

---

## ✨ Key Features

### 🎯 1. Algorithmic ATS Compatibility Scoring
- **0–100 Weighted Score Engine:** Analyzes document structure, canonical section headers, word count density, and contact signal completeness.
- **Dynamic Animated Radial Gauge:** Real-time animated SVG progress meter displaying overall ATS readiness.
- **Qualitative Verdict Badges:** Immediate feedback categorization (*Optimal*, *Good Foundation*, or *Needs Optimization*).

### 🔍 2. Deep Parsing & Keyword Gap Diagnostics
- **Native Document Support:** Extracts selectable text directly from text-based **PDF** and **DOCX** files using `PyPDF2` and `python-docx`.
- **Tech Stack & Skill Extraction:** Scans for high-demand technical keywords (Python, Django, AWS, Docker, React, SQL, CI/CD, Kubernetes, etc.) using whole-word regex tokenization.
- **Missing Keyword Recommendations:** Highlights critical missing technologies relevant to modern tech roles.
- **Raw Parsed Text Inspector:** Built-in collapsible text viewer to verify that tables or complex columns did not get scrambled during ATS ingestion.

### 🛠️ 3. Live Split-Screen Resume Builder
- **Real-Time Recruiter Preview:** Zero-dependency reactive DOM updates on the right side as you edit form fields on the left.
- **1-Click Pre-fill Demo Data:** Pre-populate an ATS-ready Senior Software Engineer profile in one click.
- **Pixel-Perfect PDF Export:** Dedicated `@media print` stylesheet that isolates the resume document and generates a clean, single-page, recruiter-approved paper resume using native browser print.
- **Quick Plain Text Copy:** One-click clipboard copy of the clean resume text.

### 🎨 4. Modern Glassmorphic Design System
- Built with **pure Vanilla CSS** (no heavy external CSS framework overhead).
- Curated dark-mode palette: Deep obsidian canvas (`#080c14`) accented with electric indigo, radiant violet, and cyber emerald.
- Polished typography using Google Fonts (**Plus Jakarta Sans** and **JetBrains Mono**).
- Micro-interactions, ambient radial background glows, drag-and-drop feedback, and toast notification alerts.

---

## 🏗️ Project Architecture

```
ResumeAnalyzerProject/
├── analyzer/                 # Core analyzer Django app
│   ├── migrations/           # Database migration files
│   ├── forms.py              # File upload forms & validators
│   ├── models.py             # Resume database models
│   ├── urls.py               # Analyzer routing endpoints
│   ├── utils.py              # Text extraction & ATS scoring logic
│   └── views.py              # Request handling & scoring heuristics
├── resume_analyzer/          # Django project configuration
│   ├── settings.py           # Core settings (Static, Media, Templates)
│   ├── urls.py               # Main URL root dispatcher
│   ├── wsgi.py               # WSGI entry point
│   └── asgi.py               # ASGI entry point
├── static/                   # Static assets
│   └── css/
│       └── styles.css        # Unified glassmorphic design system
├── templates/                # Global HTML templates
│   └── analyzer/
│       ├── base.html         # Master layout with glass navigation & toast
│       ├── home.html         # Modern hero landing page & feature grid
│       ├── upload.html       # Drag-and-drop upload & ATS diagnostic scorecard
│       └── builder.html      # Live dual-pane reactive resume workshop
├── manage.py                 # Django management command utility
└── db.sqlite3                # Local SQLite database
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- **Python 3.10+** installed on your system
- `git` version control

### 2. Clone the Repository
```bash
git clone https://github.com/<your-username>/ResumeAnalyzerProject.git
cd ResumeAnalyzerProject
```

### 3. Create & Activate Virtual Environment
**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install django PyPDF2 python-docx
```

### 5. Run Database Migrations
```bash
python manage.py migrate
```

### 6. Start the Local Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

---

## 📊 Scoring Heuristic Breakdown

The internal ATS algorithm computes a normalized score between **20 and 98** across four weighted categories:

$$\text{Total Score} = \text{Base}(30) + \text{Structure}(\le 35) + \text{Keywords}(\le 25) + \text{Length}(\le 15) + \text{Contact}(\le 15)$$

| Category | Max Points | Evaluation Signals |
| :--- | :---: | :--- |
| **Structure & Sections** | **35 pts** | Presence of canonical headers: *Experience*, *Education*, *Skills*, *Projects*, and *Summary*. |
| **Tech Keywords & Stack** | **25 pts** | Density and variety of modern engineering, cloud, database, and architectural proficiencies. |
| **Brevity & Word Count** | **15 pts** | Optimal range is **300 to 950 words** (penalizes under-developed profiles $<200$ words or bloated resumes $>1600$ words). |
| **Contact & Social Signals**| **15 pts** | Valid RFC email pattern, telephone format, and LinkedIn / GitHub profile links. |

---

## 🔒 Privacy & Security
- **In-Memory Processing:** Uploaded resumes can be parsed entirely in memory without requiring persistent third-party cloud storage.
- **Zero Third-Party Tracking:** No ad trackers, candidate data selling, or external analytics scripts.

---

## 🤝 Contributing
Contributions, suggestions, and pull requests are warmly welcome!
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---


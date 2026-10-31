# analyzer/forms.py
from django import forms

class ResumeUploadForm(forms.Form):
    file = forms.FileField(help_text="Upload a .pdf or .docx resume", required=True)

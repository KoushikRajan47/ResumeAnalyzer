from django.db import models

class Resume(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    file = models.FileField(upload_to='resumes/')
    extracted_text = models.TextField(blank=True)
    ats_score = models.IntegerField(null=True, blank=True)
    ats_friendly = models.BooleanField(null=True, blank=True)
    feedback = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name or 'Resume'} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"

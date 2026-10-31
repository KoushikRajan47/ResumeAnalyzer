from django.urls import path
from . import views

app_name = 'analyzer'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_resume, name='upload'),
    path('builder/', views.resume_builder, name='builder'),
]

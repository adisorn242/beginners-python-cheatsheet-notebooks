"""Chapter 12: Django Web Apps, Part 1 -- run this locally with `python Chapter12_Django_Web_Apps_Part1.py`.
Builds a real Django project on disk; use `python manage.py runserver` afterward to view it.
"""
import os
import subprocess

# Create the project.
subprocess.run(['django-admin', 'startproject', 'learning_log', '.'], check=True)
subprocess.run(['python', 'manage.py', 'migrate'], check=True)

# Create a superuser (non-interactive).
os.environ['DJANGO_SUPERUSER_USERNAME'] = 'admin'
os.environ['DJANGO_SUPERUSER_EMAIL'] = 'admin@example.com'
os.environ['DJANGO_SUPERUSER_PASSWORD'] = 'change-me-please'
subprocess.run(['python', 'manage.py', 'createsuperuser', '--noinput'], check=True)

# Create the learning_logs app.
subprocess.run(['python', 'manage.py', 'startapp', 'learning_logs'], check=True)

# Define the model.
model_code = '''
from django.db import models


class Topic(models.Model):
    """A topic the user is learning about."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
'''
with open('learning_logs/models.py', 'w') as f:
    f.write(model_code)

# Register the app.
settings_path = 'learning_log/settings.py'
with open(settings_path) as f:
    settings_text = f.read()
if "'learning_logs'," not in settings_text:
    settings_text = settings_text.replace(
        "INSTALLED_APPS = [",
        "INSTALLED_APPS = [\n    'learning_logs',",
    )
    with open(settings_path, 'w') as f:
        f.write(settings_text)

subprocess.run(['python', 'manage.py', 'makemigrations', 'learning_logs'], check=True)
subprocess.run(['python', 'manage.py', 'migrate'], check=True)

# Register the model with the admin site.
admin_code = '''
from django.contrib import admin
from .models import Topic

admin.site.register(Topic)
'''
with open('learning_logs/admin.py', 'w') as f:
    f.write(admin_code)

# Home page: view, template, urls.
view_code = '''
from django.shortcuts import render


def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')
'''
with open('learning_logs/views.py', 'w') as f:
    f.write(view_code)

os.makedirs('learning_logs/templates/learning_logs', exist_ok=True)
with open('learning_logs/templates/learning_logs/index.html', 'w') as f:
    f.write(
        "<p>Learning Log</p>\n"
        "<p>Learning Log helps you keep track of your learning, "
        "for any topic you're learning about.</p>\n"
    )

urls_code = '''
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
'''
with open('learning_logs/urls.py', 'w') as f:
    f.write(urls_code)

project_urls_code = '''
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('learning_logs.urls')),
]
'''
with open('learning_log/urls.py', 'w') as f:
    f.write(project_urls_code)

# Sanity check.
subprocess.run(['python', 'manage.py', 'check'], check=True)
print("Done. Run: python manage.py runserver")

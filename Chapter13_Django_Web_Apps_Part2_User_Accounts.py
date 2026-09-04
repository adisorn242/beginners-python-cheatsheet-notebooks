"""Chapter 13: Django Web Apps, Part 2 -- run this locally with `python Chapter13_Django_Web_Apps_Part2_User_Accounts.py`.
Rebuilds the project (with the owner field included from the start) and adds user accounts.
Run `python manage.py runserver` afterward to view it.
"""
import os
import subprocess

# Rebuild the project (see Part 1 for the step-by-step version).
subprocess.run(['django-admin', 'startproject', 'learning_log', '.'], check=True)
subprocess.run(['python', 'manage.py', 'migrate'], check=True)
subprocess.run(['python', 'manage.py', 'startapp', 'learning_logs'], check=True)

# Models include the owner field from the start (avoids an interactive migration prompt).
model_code = '''
from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    """A topic the user is learning about."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Entry(models.Model):
    """Learning log entries for a topic."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return f"{self.text[:50]}..."
'''
with open('learning_logs/models.py', 'w') as f:
    f.write(model_code)

settings_path = 'learning_log/settings.py'
with open(settings_path) as f:
    settings_text = f.read()
settings_text = settings_text.replace(
    "INSTALLED_APPS = [",
    "INSTALLED_APPS = [\n    'learning_logs',",
)
with open(settings_path, 'w') as f:
    f.write(settings_text)

subprocess.run(['python', 'manage.py', 'makemigrations', 'learning_logs'], check=True)
subprocess.run(['python', 'manage.py', 'migrate'], check=True)

# Home page: view, template, urls (with login/register links in the base template).
os.makedirs('learning_logs/templates/learning_logs', exist_ok=True)
with open('learning_logs/templates/learning_logs/base.html', 'w') as f:
    f.write(
        "<p><a href=\"{% url 'learning_logs:index' %}\">Learning Log</a></p>\n"
        "{% if user.is_authenticated %}"
        "<p>Hello, {{ user.username }}. "
        "<a href=\"{% url 'users:logout' %}\">log out</a></p>"
        "{% else %}"
        "<p><a href=\"{% url 'users:register' %}\">register</a> - "
        "<a href=\"{% url 'users:login' %}\">log in</a></p>"
        "{% endif %}\n"
        "{% block content %}{% endblock content %}\n"
    )
with open('learning_logs/templates/learning_logs/index.html', 'w') as f:
    f.write(
        "{% extends 'learning_logs/base.html' %}\n"
        "{% block content %}\n<p>Learning Log</p>\n{% endblock content %}\n"
    )

ll_views = '''
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from .models import Topic


def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    """Show all topics belonging to the current user."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)
'''
with open('learning_logs/views.py', 'w') as f:
    f.write(ll_views)

ll_urls = '''
from django.urls import path
from . import views

app_name = 'learning_logs'
urlpatterns = [
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
]
'''
with open('learning_logs/urls.py', 'w') as f:
    f.write(ll_urls)

with open('learning_logs/templates/learning_logs/topics.html', 'w') as f:
    f.write(
        "{% extends 'learning_logs/base.html' %}\n"
        "{% block content %}<ul>{% for t in topics %}<li>{{ t }}</li>{% endfor %}</ul>"
        "{% endblock content %}\n"
    )
with open('learning_logs/templates/learning_logs/topic.html', 'w') as f:
    f.write(
        "{% extends 'learning_logs/base.html' %}\n"
        "{% block content %}<p>{{ topic }}</p>"
        "<ul>{% for e in entries %}<li>{{ e }}</li>{% endfor %}</ul>"
        "{% endblock content %}\n"
    )

# A form for adding topics, owned by the current user.
forms_code = '''
from django import forms
from .models import Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}
'''
with open('learning_logs/forms.py', 'w') as f:
    f.write(forms_code)

# The users app: registration, login, logout.
subprocess.run(['python', 'manage.py', 'startapp', 'users'], check=True)

with open(settings_path) as f:
    settings_text = f.read()
if "'users'," not in settings_text:
    settings_text = settings_text.replace(
        "INSTALLED_APPS = [",
        "INSTALLED_APPS = [\n    'users',",
    )
    with open(settings_path, 'w') as f:
        f.write(settings_text)

users_urls = '''
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
]
'''
with open('users/urls.py', 'w') as f:
    f.write(users_urls)

users_views = '''
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def logout_view(request):
    """Log the user out."""
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))


def register(request):
    """Register a new user."""
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return HttpResponseRedirect(reverse('learning_logs:index'))

    context = {'form': form}
    return render(request, 'users/register.html', context)
'''
with open('users/views.py', 'w') as f:
    f.write(users_views)

os.makedirs('users/templates/users', exist_ok=True)
with open('users/templates/users/login.html', 'w') as f:
    f.write(
        "{% extends 'learning_logs/base.html' %}\n"
        "{% block content %}\n"
        "{% if form.errors %}<p>Your username and password didn't match.</p>{% endif %}\n"
        "<form method='post' action=\"{% url 'users:login' %}\">\n"
        "{% csrf_token %}\n{{ form.as_p }}\n"
        "<button name='submit'>log in</button>\n"
        "<input type='hidden' name='next' value=\"{% url 'learning_logs:index' %}\"/>\n"
        "</form>\n{% endblock content %}\n"
    )
with open('users/templates/users/register.html', 'w') as f:
    f.write(
        "{% extends 'learning_logs/base.html' %}\n"
        "{% block content %}\n"
        "<form method='post' action=\"{% url 'users:register' %}\">\n"
        "{% csrf_token %}\n{{ form.as_p }}\n"
        "<button name='submit'>register</button>\n"
        "</form>\n{% endblock content %}\n"
    )

project_urls = '''
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('', include('learning_logs.urls', namespace='learning_logs')),
]
'''
with open('learning_log/urls.py', 'w') as f:
    f.write(project_urls)

subprocess.run(['python', 'manage.py', 'check'], check=True)
print("Done. Run: python manage.py runserver")

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

# Create your views here.


def home_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    return render(request, 'profile/index.html', {'user': user, 'profile': profile})


def projects_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    ctx = {
        'user': user,
        'profile': profile,
        'projects': profile.project_set.all()
    }
    return render(request, 'profile/projects.html', ctx)


def skills_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    ctx = {
        'user': user,
        'profile': profile,
        'skills': profile.skills.all()
    }
    return render(request, 'profile/skills.html', ctx)
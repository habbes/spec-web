from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

# Create your views here.


def home_view(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'profile/index.html', {'user': user})


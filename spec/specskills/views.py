from django.shortcuts import render
from django.views.generic import ListView
from main.models import Skill
# Create your views here.


class IndexView(ListView):
    template_name = 'skills/index.html'
    context_object_name = 'skills'
    model = Skill

    def get_context_data(self, **kwargs):
        ctx = super(IndexView, self).get_context_data(**kwargs)
        user = self.request.user
        if user:
            ctx['user'] = user
            ctx['profile'] = user.profile
        return ctx


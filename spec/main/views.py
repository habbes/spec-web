from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Profile

# Create your views here.


class HomeView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)
        ctx['featured_profiles'] = Profile.objects.all()[:3]
        return ctx
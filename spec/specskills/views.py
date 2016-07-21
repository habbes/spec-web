from django.shortcuts import render
from django.views.generic import ListView, DetailView
from main.models import Skill
# Create your views here.


class IndexView(ListView):
    template_name = 'skills/index.html'
    context_object_name = 'skills'
    model = Skill

    def get_context_data(self, **kwargs):
        ctx = super(IndexView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated():
            ctx['user'] = user
            ctx['profile'] = user.profile
        return ctx



class SkillDetailView(DetailView):
    template_name = 'skills/detail.html'
    context_object_name = 'skill'
    model = Skill

    def get_context_data(self, **kwargs):
        ctx = super(SkillDetailView, self).get_context_data(**kwargs)
        user = self.request.user
        skill = ctx['skill']
        ctx['skill_profiles'] = skill.profile_set.all()
        if user.is_authenticated():
            ctx['user'] = user
            ctx['profile'] = user.profile
        return ctx

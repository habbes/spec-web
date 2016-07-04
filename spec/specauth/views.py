from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class AuthView(TemplateView):
    template_name = 'auth/index.html'

    def get_context_date(self, **kwargs):
        ctx = (AuthView, self).get_context_data(**kwargs)
        user = self.request.user
        if user:
            ctx['user'] = user
            ctx['profile'] = user.profile
        return ctx

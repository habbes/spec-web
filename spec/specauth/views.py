from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import logout

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


def logout_view(request):
    logout(request)
    return redirect('/')
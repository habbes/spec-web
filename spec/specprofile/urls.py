from django.conf.urls import url

from . import views

urlpatterns = [
    url('^$', views.home_view, name='home'),
    url('^projects', views.projects_view, name='projects')
]

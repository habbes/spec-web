from django.conf.urls import url

from .views import AuthView, logout_view

urlpatterns = [
    url('^$', AuthView.as_view(), name='auth'),
    url('^logout$', logout_view, name='logout')
]

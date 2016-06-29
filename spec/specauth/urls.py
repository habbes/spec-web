from django.conf.urls import url

from .views import AuthView

urlpatterns = [
    url('^$', AuthView.as_view(), name='auth'),
]
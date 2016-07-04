from django.conf.urls import url

from .views import IndexView, SkillDetailView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^(?P<pk>[^/]+)$', SkillDetailView.as_view(), name='detail'),
]


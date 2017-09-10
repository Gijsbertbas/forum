from django.conf.urls import url
from django.views.generic import RedirectView

from forum.views import *

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='index-1/')),
    url(r'^index-1/$', IndexView.as_view(), name='index'),
]


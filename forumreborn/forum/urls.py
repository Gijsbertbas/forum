from django.conf.urls import url
from django.views.generic import RedirectView

from forum.views import *

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='index-1')),
    url(r'^index-0$', RedirectView.as_view(url='../index-1')),
    url(r'^index-(?P<indno>[0-9]+)$', IndexView.as_view(), name='index'),
    url(r'^message/(?P<id>[0-9]+)$', MessageView.as_view(), name='message-view'),
]


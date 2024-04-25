from django.urls import re_path
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    re_path(r'^change/$', change),
    re_path(r'^$', index),
    re_path(r'^upload/$', TemplateView.as_view(template_name='upload.html')),
    re_path(r'^release/$', Release.as_view()),
    re_path(r'^videolist/(?P<operator>.*)/$', VideoListView.as_view()),
    re_path(r'^play/$', play),
    re_path(r'^delete/$', delete),
]
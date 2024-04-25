from django.urls import re_path
from django.views.generic import TemplateView
from .views import *


urlpatterns = [
    re_path('^register/$', TemplateView.as_view(template_name='register.html')),
    re_path('^login/$', TemplateView.as_view(template_name='login.html')),
    re_path('^logout/$', logout),
    re_path('^check_username/$', check_username),
    re_path('^generate_code/$', generate_code),
    re_path('^verify_code/$', verify_code),
    re_path('^create_account/$', create_account),
    re_path('^submit_login/$', submit_login),
    re_path('^userlist/$', UserListView.as_view()),
    re_path('^focus/$', my_focus),
    re_path('^fans/$', my_fans),
    re_path('^add_focus/$', add_focus),
    re_path('^cancel_focus/$', cancel_focus),
    re_path('^personal/$', UserInfoView.as_view()),
    re_path('^change/$', change),
]
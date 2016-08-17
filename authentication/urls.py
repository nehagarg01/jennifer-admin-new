from django.conf.urls import url

from .models import TOKEN_PATTERN
from . import views


urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^request_reset_password/$', views.request_reset_password, name='request_reset_password'),
    url(r'^reset_password/%s/$' % (TOKEN_PATTERN,), views.reset_password, name='reset_password'),
]

from django.shortcuts import render

from django.conf.urls import url,include
from . import views

from django.contrib.auth.views import login


urlpatterns = [
    #url(r'^$', views.login, name = 'login'),
    #url(r'^/', views.curator, name = 'curator'),
    url(r'^$', login, {'template_name':'administrator/login.html'}),
    ]

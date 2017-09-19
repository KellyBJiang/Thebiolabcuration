from django.shortcuts import render
from django.conf.urls import url,include
from . import views
from django.contrib.auth.views import login,logout


urlpatterns = [
    #url(r'^$', views.login, name = 'login', ),
    #url(r'^/', views.curator, name = 'curator'),
    
    # url(r'^$', login, {'template_name':'administrator/login.html'}),
    url(r'^$', views.session_login),
    url(r'^login/$', login, {'template_name':'administrator/login.html'}),
    url(r'^ad/$',views.ad,name='ad'),
    url(r'ad/assign/$', views.assign,name = 'assign'),
    url(r'ad/create/$', views.create,name = 'create'),
    #url(r'^ad/assign/', views.assign, name='assign')
    ]

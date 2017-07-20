from django.shortcuts import render
from django.conf.urls import url,include
from administrator.models import  User, Topic, Curation, Dataset, Summary
from . import views

urlpatterns = [
    url(r'^(?P<user>[0-9]+)/$', views.index, name = 'index'),
    url(r'^(?P<user>[0-9]+)/dataset/(?P<dataset_id>[0-9]+)/$', views.curation, name = 'curation'),
    ]

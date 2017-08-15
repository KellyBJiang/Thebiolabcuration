from django.shortcuts import render
from django.conf.urls import url,include
from administrator.models import  Topic, Curation, Dataset, Summary
from . import views
from django.contrib.auth.models import User

urlpatterns = [
    url(r'^(?P<user>[0-9]+)/$', views.index, name = 'index'),
    url(r'^(?P<user>[0-9]+)/dataset/(?P<dataset_id>[0-9]+)/(?P<curation_id>[0-9]+)/$', views.curation, name = 'curation'),
    ]

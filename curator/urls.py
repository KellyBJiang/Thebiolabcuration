from django.shortcuts import render
from django.conf.urls import url,include
from administrator.models import  Topic, Curation, Dataset, Summary
from . import views
from django.contrib.auth.models import User
# For iframe
from django.views.generic import TemplateView
urlpatterns = [
        url(r'^(?P<user>[0-9]+)/$', views.index, name = 'index'),
        url(r'^(?P<user>[0-9]+)/dataset/(?P<dataset_id>[0-9]+)/(?P<curation_id>[0-9]+)/$', views.curation, name = 'curation'),
        url(r'^(?P<user>[0-9]+)/dataset/(?P<dataset_id>[0-9]+)/(?P<curation_id>[0-9]+)/ncbi.html/$', views.ncbi, name='ncbi'),
        url(r'^(?P<user>[0-9]+)/dataset/(?P<dataset_id>[0-9]+)/(?P<curation_id>[0-9]+)/pubmed.html/$', views.pubmed, name='pubmed'),
        url(r'^(?P<user>[0-9]+)/dataset/(?P<dataset_id>[0-9]+)/(?P<curation_id>[0-9]+)/pmc.html/$', views.pmc, name='pmc'),
    ]

from django.shortcuts import render
from .models import  User, Topic, Curation, Dataset, Summary

# Create your views here.
def login(request):
    return render(request, 'administrator/login.html')
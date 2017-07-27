from django.shortcuts import render
from .models import  User, Topic, Curation, Dataset, Summary
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.
def login(request):
    template = loader.get_template('administrator/login.html')
    #return render(request, 'administrator/login.html')
    return HttpResponse(template.render(request))
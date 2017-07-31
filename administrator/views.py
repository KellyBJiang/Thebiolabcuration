from django.shortcuts import render,redirect
from .models import  User, Topic, Curation, Dataset, Summary
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth


from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    # name=request.user.username
    if user is not None and user.is_active:
        auth.login(request, user)# add user to SESSION
    else:
    # Show an error page
       return HttpResponseRedirect("/account/invalid/")
       
@login_required       
def logged_in(request):
    #role judgement
    if request.user.is_staff: #admin
         return HttpResponseRedirect('/admin/%d/'%request.user.id)
    else: #curator
        return HttpResponseRedirect('/curator/%d/'%request.user.id)

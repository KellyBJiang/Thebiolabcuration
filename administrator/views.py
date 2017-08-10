from django.shortcuts import render,redirect
from .models import  Topic, Curation, Dataset, Summary
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm

# from .forms import MyUserCreationForm
from .forms import UserRegisterForm

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
         return HttpResponseRedirect('/admin/')
    else: #curator
        return HttpResponseRedirect('/curator/%d/'%request.user.id)

def logged_out(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def register(request):
    title="Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit = False)
        password = form.cleaned_data.get('password1')
        user.set_password(password)
        user.save()
        return redirect('/')
        
    else:
        context = {
            "form": form,
            "title" : title
        }
        return render(request, "administrator/register.html",context)
    

def assign(request):
    datasets = Dataset.objects.all()
    users = User.objects.all()
    context = {
        'users': users,
        'datasets': datasets,
        'datasets_count': datasets.count(),
    }
    template = loader.get_template("administrator/assign.html")
    return HttpResponse(template.render(context, request))
    
    
    
    
def ad(request):
    return render(request, "administrator/ad.html")
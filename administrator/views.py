from django.shortcuts import render,redirect
from .models import  Topic, Curation, Dataset, Summary
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import datetime
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
         return HttpResponseRedirect('/ad/')
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
    
@login_required(login_url='/') 
def assign(request):
    if request.user.is_staff :
        datasets = Dataset.objects.all()
        users = User.objects.filter(is_staff=False)
        topics = Topic.objects.all()
        context = {
            'users': users,
            'datasets': datasets,
            'topics':topics
        }
        template = loader.get_template("administrator/assign.html")
        # Get the selected id of topic, user,  datasets
        selected_datasets=request.POST.getlist('selected_datasets[]')
        selected_topic = request.POST.get('selected_topic')
        selected_users = request.POST.getlist('selected_users[]')
        print selected_datasets
        print selected_topic
        print selected_users
        today = datetime.datetime.today()
        if len(selected_datasets) != 0 and len(selected_users)!=0:
            #SEL_DATASETS = Dataset.objects.values_list('id',flat=True).filter(pk__in = selected_datasets)
            #Create curation table
            curation = [ ]
            for sel_d in selected_datasets:
                for sel_u in selected_users:
                    if Curation.objects.filter(topic_id = selected_topic, data_id = sel_d, user_id = sel_u).count() == 0:
                        curation = Curation()
                        curation.topic_id = Topic.objects.get(id=selected_topic)
                        curation.data_id = Dataset.objects.get(id = sel_d)
                        curation.user_id =  User.objects.get(id=sel_u)
                        curation.result = 'N'
                        curation.comment = ""
                        curation.submit = 0
                        curation.date = today
                        curation.save()
                        print curation
            # return HttpResponse(template.render(context, request))
    
        return HttpResponse(template.render(context, request))
    else:
         return HttpResponseRedirect('/')


@login_required(login_url='/') 
def ad(request):
    if request.user.is_staff :
        return render(request, "administrator/ad.html")
    else:
        return HttpResponseRedirect('/')
        
        
        
        
@login_required(login_url='/')         
def create(request):
    if request.user.is_staff :
        return render(request, "administrator/adpage/create.html")
    else:
        return HttpResponseRedirect('/')
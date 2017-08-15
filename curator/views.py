from django.shortcuts import render, redirect
from administrator.models import   Topic, Curation, Dataset, Summary
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from .forms import CurationFrom
from django.utils import timezone
import requests
import json 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required(login_url='/')
def index(request,user):
    c_ids = Curation.objects.filter(user_id = user,submit = False) #to do curation
    c_s = Curation.objects.filter(user_id = user,submit = True)
    c_u = Curation.objects.filter(user_id = user,result='U')

    curation_data_ids = Curation.objects.values_list('data_id',flat=True).filter(user_id = user,submit = False)
    curation_submitted = Curation.objects.values_list('data_id',flat=True).filter(user_id = user,submit = True)
    curation_undicided = Curation.objects.values_list('data_id',flat=True).filter(user_id = user,result='U')
    
    datasets = Dataset.objects.filter(pk__in = curation_data_ids) #to do list
    datasets_submitted = Dataset.objects.filter(pk__in = curation_submitted) #submitted list
    datasets_undicided = Dataset.objects.filter(pk__in = curation_undicided) #undicided list
    
    template = loader.get_template('curator/index.html')
    
    context = {
        'c_ids':c_ids, #to do curation id
        'c_s':c_s,#submitted curation id
        'c_u':c_u,# undecided curation id
        'curation_data_ids':curation_data_ids, #To do curation_dataset_id
        'curation_submitted':curation_submitted, # submited curations id
        'curation_undicided' : curation_undicided, # undecided curations id
        'datasets':datasets, #to do list
        'datasets_count':c_ids.count(),
        'datasets_submitted':datasets_submitted,
        'datasets_submitted_count':c_s.count(),
        'datasets_undicided':datasets_undicided,
        'datasets_undicided_count':c_u.count(),
        'user_id':user,
    }
    if request.user.id == int(user) :
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/')
 
        
        
        
@login_required 
def curation(request,user,dataset_id,curation_id):
    
    #get the id of the next unsubmitted one
    c_ids=Curation.objects.filter(user_id = user,submit = False)#list of to do curation
    
    # curation_data_ids = Curation.objects.values_list('data_id',flat=True).filter(user_id = user,submit = False)
    # datasets_next_unsubmitted = Dataset.objects.filter(pk__in = curation_data_ids) #this is actually to do list
    
    #current dataset
    dataset = Dataset.objects.get(pk = dataset_id)
    pubmedid = Dataset.objects.values_list('pubNo',flat = True).get(pk = dataset_id)
    
    #get the topic and the comment,result, submit state sof the current dataset
    topic_id = Curation.objects.values_list('topic_id',flat = True).get(pk=curation_id)
    topic = Topic.objects.get(pk = topic_id)
    cur_comment = Curation.objects.values_list('comment',flat = True).get(pk=curation_id)
    cur_result = Curation.objects.values_list('result',flat = True).get(pk=curation_id)
    cur_submit = Curation.objects.values_list('submit',flat = True).get(pk=curation_id)
    
    #topic_id = Curation.objects.values_list('topic_id',flat = True).get(user_id = user, data_id = dataset_id)
    # topic = Topic.objects.get(pk = topic_id)
    # cur_comment = Curation.objects.values_list('comment',flat = True).get(user_id = user, data_id = dataset_id)
    # cur_result = Curation.objects.values_list('result',flat = True).get(user_id = user, data_id = dataset_id)
    # cur_submit = Curation.objects.values_list('submit',flat = True).get(user_id = user, data_id = dataset_id)
    
    
    
    #which template to use:
    template = loader.get_template('curator/curation.html')
    
    #Get data from ID convertor
    convert_url = 'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids='+pubmedid+'&idtype=pmid&format=json&versions=yes&showaiid=no&tool=my_tool&email=my_email%40example.com&.submit=Submit'
    convert_pmc=requests.get(convert_url)#get the jsonfile including the converted pmc_id 
    jsonString=convert_pmc.content # pmc id is under the tag content
    
    
    #if request.method == "POST" and 'highlight' in request.POST:
    url='https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE84724'
    iframe = requests.get(url).content
    
    if request.method == "POST":
        curation = Curation.objects.get(user_id = user, data_id = dataset_id, topic_id=topic_id)
        form = CurationFrom(request.POST or None)
        if form.is_valid() and request.user.is_authenticated:
            curation.result = form.cleaned_data.get("result")
            curation.comment = form.cleaned_data.get("comment")
            curation.submit = True
            curation.date = timezone.now()
            curation.save()
            if c_ids.count() > 0:
                return redirect("curation",user = user,dataset_id = c_ids[0].data_id_id,curation_id = int(c_ids[0].pk))
            else:
                return redirect("index", user = user)
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    else:
        form = CurationFrom(initial={'comment':cur_comment, 'result' : cur_result})
        context = {
                'dataset':dataset,
                'user_id':user,
                'topic' : topic,
                'form':form,
                'cur_comment':cur_comment,
                'cur_result':cur_result,
                'cur_submit':cur_submit,
                'jsonString':jsonString,
                'iframe_content':iframe,
            }
        return HttpResponse(template.render(context, request))
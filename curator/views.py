from django.shortcuts import render, redirect
from administrator.models import   Topic, Curation, Dataset, Summary
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from .forms import CurationFrom
from django.utils import timezone
import requests
import json 
from django.contrib.auth.models import User

# Create your views here.
def index(request,user):
    #curation_data_ids = Curation.objects.values_list('data_id',flat=True).get(user_id = user)
    #datasets = Dataset.objects.filter(pk__in = [curation_data_ids])
    curation_data_ids = Curation.objects.values_list('data_id',flat=True).filter(user_id = user,submit = False)
    curation_submitted = Curation.objects.values_list('data_id',flat=True).filter(user_id = user,submit = True)
    curation_undicided = Curation.objects.values_list('data_id',flat=True).filter(user_id = user,result='U')
    datasets = Dataset.objects.filter(pk__in = curation_data_ids)
    datasets_submitted = Dataset.objects.filter(pk__in = curation_submitted)
    datasets_undicided = Dataset.objects.filter(pk__in = curation_undicided)
    template = loader.get_template('curator/index.html')
    context = {
        'curation_data_ids':curation_data_ids,
        'curation_submitted':curation_submitted,
        'curation_undicided' : curation_undicided,
        'datasets':datasets,
        'datasets_submitted':datasets_submitted,
        'datasets_undicided':datasets_undicided,
        'user_id':user,
    }
    return HttpResponse(template.render(context, request))
    

def curation(request,user,dataset_id):
    dataset = Dataset.objects.get(pk = dataset_id)
    pubmedid = Dataset.objects.values_list('pubNo',flat = True).get(pk = dataset_id)
    
    # topic_id = Dataset.objects.values_list('topic_id',flat=True).get(pk = dataset_id)
    topic_id = Curation.objects.values_list('topic_id',flat = True).get(user_id = user, data_id = dataset_id)
    cur_comment = Curation.objects.values_list('comment',flat = True).get(user_id = user, data_id = dataset_id)
    cur_result = Curation.objects.values_list('result',flat = True).get(user_id = user, data_id = dataset_id)
    cur_submit = Curation.objects.values_list('submit',flat = True).get(user_id = user, data_id = dataset_id)
    
    topic = Topic.objects.get(pk = topic_id)
    template = loader.get_template('curator/curation.html')
    
    
    
    #Get data from ID convertor
    convert_url = 'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids='+pubmedid+'&idtype=pmid&format=json&versions=yes&showaiid=no&tool=my_tool&email=my_email%40example.com&.submit=Submit'
    #str = 'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids=22863743&idtype=pmid&format=json&versions=yes&showaiid=no&tool=my_tool&email=my_email%40example.com&.submit=Submit'
    convert_pmc=requests.get(convert_url)
    jsonString=convert_pmc.content  
    
    
    
    if request.method == "POST":
        curation = Curation.objects.get(user_id = user, data_id = dataset_id, topic_id=topic_id)
        form = CurationFrom(request.POST or None)
        if form.is_valid():
            curation.result = form.cleaned_data.get("result")
            curation.comment = form.cleaned_data.get("comment")
            curation.submit = True
            curation.date = timezone.now()
            curation.save()
            #return redirect("curator/"+str(user))
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
                
                
            }
        return HttpResponse(template.render(context, request))
from django.shortcuts import render
from administrator.models import  User, Topic, Curation, Dataset, Summary
from django.template import loader
from django.http import HttpResponse


# Create your views here.
def index(request,user):
    #curation_data_ids = Curation.objects.values_list('data_id',flat=True).get(user_id = user)
    #datasets = Dataset.objects.filter(pk__in = [curation_data_ids])
    curation_data_ids = Curation.objects.values_list('data_id',flat=True).filter(user_id = user,submit = False)
    datasets = Dataset.objects.filter(pk__in = curation_data_ids)
    template = loader.get_template('curator/index.html')
    context = {
        'curation_data_ids':curation_data_ids,
        'datasets':datasets,
        'user_id':user,
    }
    return HttpResponse(template.render(context, request))
    

def curation(request,user,dataset_id):
    dataset = Dataset.objects.get(pk = dataset_id)
    topic_id = Dataset.objects.values_list('topic_id',flat=True).get(pk = dataset_id)
    topic = Topic.objects.get(pk = topic_id)
    template = loader.get_template('curator/curation.html')
    context = {
        'dataset':dataset,
        'user_id':user,
        'topic' : topic,
    }
    return HttpResponse(template.render(context, request))
    

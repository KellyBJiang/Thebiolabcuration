from django.shortcuts import render, redirect
from administrator.models import  User, Topic, Curation, Dataset, Summary
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from .forms import CurationFrom
from django.utils import timezone


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
            # form = CurationFrom()
            # context = {
            #     'dataset':dataset,
            #     'user_id':user,
            #     'topic' : topic,
            #     'form':form,
            # }
            # return HttpResponse(template.render(context, request))
    else:
        form = CurationFrom(request.POST or None)
        context = {
                'dataset':dataset,
                'user_id':user,
                'topic' : topic,
                'form':form,
            }
        return HttpResponse(template.render(context, request))
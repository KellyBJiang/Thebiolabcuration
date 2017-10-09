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
from django.db import connection
# from django.contrib import messages


# highlight
import urllib2
import cookielib
from bs4 import BeautifulSoup

#parser json file
import json
from django.views.decorators.csrf import csrf_exempt

#To get pmc html, need selenium
from selenium import webdriver

#split string
import re

#Pagintion on backend
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#pass json object to django
from django.core import serializers







#INDEX PAGE
@login_required(login_url='/')
def index(request,user):
    
    c_ids = Curation.objects.filter(user_id = user,submit = False) #to do curation
    c_s = Curation.objects.filter(user_id = user,submit = True)
    c_u = Curation.objects.filter(user_id = user,result='U')

    curation_data_ids = Curation.objects.values_list('data_id',flat=True).filter(user_id = user,submit = False)
    curation_submitted = Curation.objects.values_list('data_id',flat=True).filter(user_id = user,submit = True)
    curation_undecided = Curation.objects.values_list('data_id',flat=True).filter(user_id = user,result='U')
    
    datasets = Dataset.objects.filter(pk__in = curation_data_ids) #to do list
    datasets_submitted = Dataset.objects.filter(pk__in = curation_submitted) #submitted list
    datasets_undecided = Dataset.objects.filter(pk__in = curation_undecided) #undicided list
    topic = Topic.objects.all()
    
    #select topic,items_per_page post
    select_topic = request.session.get('select_topic',-1)
    items_per_page = request.session.get('items_per_page',10)
    nav = request.session.get('nav',0)
    
   
    
    if request.method == 'POST':
        select_topic = request.POST.get('selector',  request.session.get('select_topic',-1)) 
        request.session['select_topic'] = select_topic
        
        items_per_page = request.POST.get('items_per_page',  request.session.get('items_per_page',10)) 
        request.session['items_per_page'] = items_per_page  
        
        nav = request.POST.get('navbar',request.session.get('nav',0))
        request.session['nav'] = nav  
        
        
    
    select_topic = int(select_topic)
    user_topic_set = Curation.objects.values_list('topic_id',flat = True).filter(user_id = user). distinct()   
        
        
    nav = int(nav)
    if nav == 0:
        if select_topic == -1:
            print "nav = 0, select = -1"
            c_ids = Curation.objects.filter(user_id = user,submit = False) #to do curation
        else:
            print "nav = 0, select != -1"
            c_ids = Curation.objects.filter(user_id = user,topic_id = select_topic, submit = False) #to do curation
            datasets = datasets.filter(topic = select_topic)
            
        curation = c_ids
        dataset = datasets
        print "TODO curation:"
        print curation.count()
    elif nav == 1:
        if select_topic == -1:
            print "nav = 1, select = -1"
            c_s = Curation.objects.filter(user_id = user,submit = True)
        else:
            print "nav = 1, select != -1"
            c_s = Curation.objects.filter(user_id = user,topic_id = select_topic, submit = True)
            datasets_submitted = datasets_submitted.filter(topic = select_topic)
            
        curation = c_s
        dataset = datasets_submitted
    else:
        if select_topic == -1:
            print "nav = 2, select = -1"
            c_u = Curation.objects.filter(user_id = user,result='U')
        else:
            print "nav = 2, select != -1"
            c_u = Curation.objects.filter(user_id = user,topic_id = select_topic, result='U')
            datasets_undecided = datasets_undecided.filter(topic = select_topic)
            
        curation = c_u
        dataset = datasets_undecided


    #pagination    
    page = request.GET.get('page', 1)
    paginator = Paginator(dataset, items_per_page)
    try:
        dataset = paginator.page(page)
    except PageNotAnInteger:
        dataset = paginator.page(1)
    except EmptyPage:
        dataset = paginator.page(paginator.num_pages)

        
        
        
        

    template = loader.get_template('curator/index.html')

    count = curation.count()
    context = {
        'curation' :curation,
        'dataset' : dataset,
        'select_topic' : int(select_topic),
        'items_per_page' : int(items_per_page),
        'topics':topic,
        'user_id':user,
        'nav':nav,
        "count":count,
        "user_topic_set":user_topic_set,
    }
    
    if request.user.id == int(user) :
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/')
 
        
        
@csrf_exempt    
@login_required 
def curation(request,user,dataset_id,curation_id):
    
    #get the id of the next unsubmitted one
    c_ids=Curation.objects.filter(user_id = user,submit = False)#list of to do curation
    # curation_data_ids = Curation.objects.values_list('data_id',flat=True).filter(user_id = user,submit = False)
    # datasets_next_unsubmitted = Dataset.objects.filter(pk__in = curation_data_ids) #this is actually to do list
    
    #current dataset
    dataset = Dataset.objects.get(pk = dataset_id)
    accNo= Dataset.objects.values_list('accNo',flat = True).get(pk = dataset_id)
    pubmedid = Dataset.objects.values_list('pubNo',flat = True).get(pk = dataset_id)
    
    #get the topic and the comment,result, submit state sof the current dataset
    topic_id = Curation.objects.values_list('topic_id',flat = True).get(pk=curation_id)
    topic = Topic.objects.get(pk = topic_id)
    cur_comment = Curation.objects.values_list('comment',flat = True).get(pk=curation_id)
    cur_result = Curation.objects.values_list('result',flat = True).get(pk=curation_id)
    cur_submit = Curation.objects.values_list('submit',flat = True).get(pk=curation_id)
    
    
    
    #define template:
    template = loader.get_template('curator/curation.html')
    

    #Python download webpage
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
     
    
    #highlight on NCBI page
    highlight = []
    soup_pattern = []
    highlight_keywords = []

    if topic.highlihgt != None:
        highlight.append(topic.highlihgt.encode('utf-8')) 
    else:
        highlight.append('');
    if dataset.highlight != None:
        highlight.append(dataset.highlight.encode('utf-8')) 
    else:
        highlight.append('');
    if dataset.keywords != None:
        highlight.append(dataset.keywords.encode('utf-8'))
    else:
         highlight.append('');

    # soup_pattern.append(re.split(r'[;,\s]\s*' ,highlight[0]))
    # soup_pattern.append(re.split(r'[;,\s]\s*' ,highlight[1])) 
    # soup_pattern.append(re.split(r'[;,\s]\s*' ,highlight[2]))
    soup_pattern.append(re.split(';' ,highlight[0]))
    soup_pattern.append(re.split(';' ,highlight[1])) 
    soup_pattern.append(re.split(';',highlight[2]))
    
    # REGULAR EXPRESSION highlight keywords
    highlight_keywords.append('') 
    highlight_keywords.append('')
    highlight_keywords.append('')
    regex = []
    for i in range(3):
        if len(soup_pattern) != 0:
            for phrase in soup_pattern[i]:
                if len(phrase) >= 3 :
                    highlight_keywords[i]+="(\\b"+str(phrase)+"(s?)"+"\\b)|"
            highlight_keywords[i] += '\b'
            regex.append(re.compile(highlight_keywords[i], re.IGNORECASE))
    
    
    
    
    #Download ncbi page, replace the wrong urls
    url_n = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc="+accNo
    req_n = urllib2.Request(url_n)
    operate_n = opener.open(req_n)
    msg_n = operate_n.read() #content of ncbi page
    document_n = 'curator/templates/curator/ncbi.html'  
    file_ = open(document_n,'w')  
    msg_n = msg_n.replace('src="','src="https://www.ncbi.nlm.nih.gov')
    msg_n = msg_n.replace('href="/geo','href="https://www.ncbi.nlm.nih.gov/geo')
    msg_n = msg_n.replace('href="/Taxonomy','href="https://www.ncbi.nlm.nih.gov/Taxonomy')
    msg_n = msg_n.replace('href="/pubmed/', 'href="https://www.ncbi.nlm.nih.gov/pubmed/')
    # replace requires beautiful soup
    soup_n = BeautifulSoup(msg_n,"html5lib")
    for li in soup_n.find_all('li'):
        li.decompose()
    for f in soup_n.find_all('form'):
        f.decompose()
    soup_string_n = str(soup_n)
    #highlight ncbi
    i = 0; output=""
    for m in regex[0].finditer(soup_string_n):
        output += "".join([soup_string_n[i:m.start()],
                           "<mark style='background-color:#ffb7b7;'>", #topic : red
                           soup_string_n[m.start():m.end()],
                           "</mark>"])
        i = m.end() 
    soup_string_n= "".join([output, soup_string_n[i:]])
    
    i = 0; output=""
    for m in regex[1].finditer(soup_string_n):
        output += "".join([soup_string_n[i:m.start()],
                           "<mark style='background-color:#a8d1ff;'>", #hight. blue
                           soup_string_n[m.start():m.end()],
                           "</mark>"])
        i = m.end() 
    soup_string_n= "".join([output, soup_string_n[i:]])
    
    i = 0; output=""
    for m in regex[2].finditer(soup_string_n):
        output += "".join([soup_string_n[i:m.start()],
                           "<mark style='background-color:#fff2a8;'>", #keyword yellow
                           soup_string_n[m.start():m.end()],
                           "</mark>"])
        i = m.end() 
    soup_string_n= "".join([output, soup_string_n[i:]])
    
    
    file_.write(soup_string_n)
    file_.close()
    # Get pmc number
    convert_url = 'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids='+pubmedid+'&idtype=pmid&format=json&versions=yes&showaiid=no&tool=my_tool&email=my_email%40example.com&.submit=Submit'
    convert_pmc=requests.get(convert_url)#get the jsonfimessages.info(request, "Submit success")le including the converted pmc_id 
    jsonString=convert_pmc.content # pmc id is under the tag content
    j = json.loads(jsonString)

    # Submit curation result
    if request.method == "POST":
        curation = Curation.objects.get(user_id = user, data_id = dataset_id, topic_id=topic_id)
        form = CurationFrom(request.POST or None)
        if form.is_valid() and request.user.is_authenticated:
            curation.result = form.cleaned_data.get("result")
            curation.comment = form.cleaned_data.get("comment")
            curation.submit = True
            curation.date = timezone.now()
            curation.save()
            connection.close()
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
                # 'pmc_delay': pmc_delay,
            }
        return HttpResponse(template.render(context, request))
        
        
def ncbi(request,user,dataset_id,curation_id):
    template = loader.get_template('curator/ncbi.html')
    return HttpResponse(template.render(request))
    
    
def pubmed(request,user,dataset_id,curation_id):
    pubmedid = Dataset.objects.values_list('pubNo',flat = True).get(pk = dataset_id)
    # Get highlight keywords
    topic_id = Curation.objects.values_list('topic_id',flat = True).get(pk=curation_id)
    topic = Topic.objects.get(pk = topic_id)
    dataset = Dataset.objects.get(pk = dataset_id)
    #highlight on pubmed page

    highlight = []
    soup_pattern = []
    highlight_keywords = []
    
    if topic.highlihgt != None:
        highlight.append(topic.highlihgt.encode('utf-8')) 
    else:
        highlight.append('');
    if dataset.highlight != None:
        highlight.append(dataset.highlight.encode('utf-8')) 
    else:
        highlight.append('');
    if dataset.keywords != None:
        highlight.append(dataset.keywords.encode('utf-8'))
    else:
         highlight.append('');
         
    # soup_pattern.append(re.split(r'[;,\s]\s*' ,highlight[0]))
    # soup_pattern.append(re.split(r'[;,\s]\s*' ,highlight[1])) 
    # soup_pattern.append(re.split(r'[;,\s]\s*' ,highlight[2]))
    soup_pattern.append(re.split(';' ,highlight[0]))
    soup_pattern.append(re.split(';' ,highlight[1])) 
    soup_pattern.append(re.split(';',highlight[2]))
    # REGULAR EXPRESSION highlight keywords
    highlight_keywords.append('') 
    highlight_keywords.append('')
    highlight_keywords.append('')
    
    regex = []
    for i in range(3):
        if len(soup_pattern) != 0:
            for phrase in soup_pattern[i]:
                if len(phrase) >= 3 :
                    highlight_keywords[i]+="(\\b"+str(phrase)+"(s?)"+"\\b)|"
            highlight_keywords[i] += '\b'
            regex.append(re.compile(highlight_keywords[i], re.IGNORECASE))
    
    #Download pubmed page
    url = 'https://www.ncbi.nlm.nih.gov/pubmed/'+pubmedid
    response = urllib2.urlopen(url)
    msg_pmed = response.read()
    
    # Highlight on Pubmed page
    i = 0; output=""
    for m in regex[0].finditer(msg_pmed):
        output += "".join([msg_pmed[i:m.start()],
                          "<mark style='background-color:#ffb7b7;'>",
                          msg_pmed[m.start():m.end()],
                          "</mark>"])
        i = m.end() 
    msg_pmed= "".join([output, msg_pmed[i:]])

    i = 0; output=""
    for m in regex[1].finditer(msg_pmed):
        output += "".join([msg_pmed[i:m.start()],
                          "<mark style='background-color:#a8d1ff;'>",
                          msg_pmed[m.start():m.end()],
                          "</mark>"])
        i = m.end() 
    msg_pmed= "".join([output, msg_pmed[i:]])

    
    
    i = 0; output=""
    for m in regex[2].finditer(msg_pmed):
        output += "".join([msg_pmed[i:m.start()],
                          "<mark style='background-color:#fff2a8;'>",
                          msg_pmed[m.start():m.end()],
                          "</mark>"])
        i = m.end() 
    msg_pmed= "".join([output, msg_pmed[i:]])






    f = open('curator/templates/curator/pubmed.html', 'w')
    f.write(msg_pmed)
    f.close()
    template = loader.get_template('curator/pubmed.html')
    return HttpResponse(template.render(request))
    
    
def pmc(request,user,dataset_id,curation_id):
    pubmedid = Dataset.objects.values_list('pubNo',flat = True).get(pk = dataset_id)
    
    convert_url = 'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids='+pubmedid+'&idtype=pmid&format=json&versions=yes&showaiid=no&tool=my_tool&email=my_email%40example.com&.submit=Submit'
    convert_pmc=requests.get(convert_url)#get the jsonfile including the converted pmc_id 
    jsonString=convert_pmc.content # pmc id is under the tag content
    j = json.loads(jsonString)
    
    # Get highlight keywords
    topic_id = Curation.objects.values_list('topic_id',flat = True).get(pk=curation_id)
    topic = Topic.objects.get(pk = topic_id)
    dataset = Dataset.objects.get(pk = dataset_id)
    #highlight on pmc page
    
    highlight = []
    soup_pattern = []
    highlight_keywords = []
    if topic.highlihgt != None:
        highlight.append(topic.highlihgt.encode('utf-8')) 
    else:
        highlight.append('');
    if dataset.highlight != None:
        highlight.append(dataset.highlight.encode('utf-8')) 
    else:
        highlight.append('');
    if dataset.keywords != None:
        highlight.append(dataset.keywords.encode('utf-8'))
    else:
         highlight.append('');
    soup_pattern.append(re.split(';' ,highlight[0]))
    soup_pattern.append(re.split(';' ,highlight[1])) 
    soup_pattern.append(re.split(';' ,highlight[2]))
    # REGULAR EXPRESSION highlight keywords
    highlight_keywords.append('') 
    highlight_keywords.append('')
    highlight_keywords.append('')
    
    regex = []
    for i in range(3):
        if len(soup_pattern) != 0:
            for phrase in soup_pattern[i]:
                if len(phrase) >= 3 :
                    highlight_keywords[i]+="(\\b"+str(phrase)+"(s?)"+"\\b)|"
            highlight_keywords[i] += '\b'
            regex.append(re.compile(highlight_keywords[i], re.IGNORECASE))
    
    
    
    
    #download the pmc page
    # pmc_delay = 0
    if j.get("records") != None:
        if j["records"][0].get("pmcid") != None:
            pmcnum = j["records"][0]["pmcid"]
            #pmc website refuse download , so use PhantomJS to crawl
            msg_pmc_obj = webdriver.PhantomJS( service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'] )
            url_pmc = "https://www.ncbi.nlm.nih.gov/pmc/articles/"+pmcnum
            msg_pmc_obj.get(url_pmc)
            msg_pmc=msg_pmc_obj.page_source.encode('utf-8')
            cov = open("curator/templates/curator/pmc.html","w")
            #check if the actual paper is delayed
            pmc_delay = msg_pmc.find("This article has a delayed release")
            # Highlight on PMC page
            
            i = 0; output=""
            for m in regex[0].finditer(msg_pmc):
                output += "".join([msg_pmc[i:m.start()],
                                  "<mark style='background-color:#ffb7b7;'>",
                                  msg_pmc[m.start():m.end()],
                                  "</mark>"])
                i = m.end() 
            msg_pmc= "".join([output, msg_pmc[i:]])
            
            i = 0; output=""
            for m in regex[1].finditer(msg_pmc):
                output += "".join([msg_pmc[i:m.start()],
                                  "<mark style='background-color:#a8d1ff;'>",
                                  msg_pmc[m.start():m.end()],
                                  "</mark>"])
                i = m.end() 
            msg_pmc= "".join([output, msg_pmc[i:]])
            
            i = 0; output=""
            for m in regex[2].finditer(msg_pmc):
                output += "".join([msg_pmc[i:m.start()],
                                  "<mark style='background-color:#fff2a8;'>",
                                  msg_pmc[m.start():m.end()],
                                  "</mark>"])
                i = m.end() 
            msg_pmc= "".join([output, msg_pmc[i:]])
            
            cov.write(msg_pmc)
            msg_pmc_obj.quit()
            cov.close()
            
    template = loader.get_template('curator/pmc.html')
    context = {
                'pmc_delay': pmc_delay,
            }
    print "pmc_delay"
    print pmc_delay
    return HttpResponse(template.render(context, request))

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime   


# class User(models.Model) : 
#     name = models.CharField(max_length = 140)
#     pw = models.CharField(max_length = 20)
#     email = models.CharField(max_length = 50)
#     role = models.CharField(max_length = 10)
#     expert = models.BooleanField(default=False)
#     institute = models.CharField(max_length = 140)
#     time = models.DateTimeField(default=None, blank=True, null=True)
#     online = models.BooleanField(default=False)
#     description = models.TextField(default=None, blank=True, null=True)
#     def __str__(self) :
#         return self.name
        
class Topic(models.Model):
    topic = models.CharField(max_length = 200)
    highlihgt = models.CharField(default="",max_length = 300)
    date = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self) :
        return self.topic
        
class Dataset(models.Model) :
    title = models.TextField(default=None, blank=True, null=True)
    accNo = models.TextField(default="", blank=True, null=True)
    pubNo = models.TextField(default="", blank=True, null=True)
    highlight = models.TextField(default="", blank=True, null=True)
    keywords = models.TextField(default="", blank=True, null=True)
    topic = models.IntegerField(default = 0)
    # def __str__(self) :
    #     return self.title
    def __unicode__(self):
        return u'%s' % (self.title)
    

class Curation(models.Model):
    RESULT_CHOICES = (
    ('Y', 'Yes'),
    ('N', 'No'),
    ('U', 'Undecided'),)
    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    topic_id = models.ForeignKey('Topic',on_delete=models.CASCADE,)
    data_id = models.ForeignKey('Dataset', on_delete = models.CASCADE,)
    user_id = models.ForeignKey(User)
    result = models.CharField(max_length=1,choices=RESULT_CHOICES, default="N")
    comment = models.TextField(default="Leave your Comment", blank=True, null=True)
    submit = models.BooleanField(default = False)
    date = models.DateTimeField(default=datetime.now, blank=True)
    
    # def __str__(self):
    #     return self.comment
    
    def __unicode__(self):
         return u'Comment: %s' % self.comment
    
class Summary(models.Model):
    topic_id = models.ForeignKey('Topic',on_delete=models.CASCADE)
    data_id = models.ForeignKey('Dataset', on_delete = models.CASCADE,)
    finalresult = models.BooleanField(default = False)
    
    

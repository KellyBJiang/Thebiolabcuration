from __future__ import unicode_literals

from django.db import models



class User(models.Model) : 
    name = models.CharField(max_length = 140)
    pw = models.CharField(max_length = 20)
    email = models.CharField(max_length = 50)
    role = models.CharField(max_length = 10)
    expert = models.BooleanField(default=False)
    institute = models.CharField(max_length = 140)
    time = models.DateTimeField(default=None, blank=True, null=True)
    online = models.BooleanField(default=False)
    description = models.TextField(default=None, blank=True, null=True)
    def __str__(self) :
        return self.name
        
class Topic(models.Model):
    topic = models.CharField(max_length = 200)
    date = models.DateTimeField(default=None, blank=True, null=True)
    
    def __str__(self) :
        return self.topic
        
class Dataset(models.Model) :
    topic_id =  models.ForeignKey('Topic',on_delete=models.CASCADE,)
    title = models.TextField()
    content = models.TextField()
    
    def __str__(self) :
        return self.title
    

class Curation(models.Model):
    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    topic_id = models.ForeignKey('Topic',on_delete=models.CASCADE,)
    data_id = models.ForeignKey('Dataset', on_delete = models.CASCADE,)
    user_id = models.ForeignKey('User', on_delete = models.CASCADE,) 
    result = models.BooleanField(choices=BOOL_CHOICES,default=False)
    comment = models.TextField(default="Comment", blank=True, null=True)
    submit = models.BooleanField(default = False)
    date = models.DateTimeField(default=None, blank=True, null=True)
    def __str__(self):
        return self.comment
    
class Summary(models.Model):
    topic_id = models.ForeignKey('Topic',on_delete=models.CASCADE)
    data_id = models.ForeignKey('Dataset', on_delete = models.CASCADE,)
    finalresult = models.BooleanField(default = False)
    
    

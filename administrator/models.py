from __future__ import unicode_literals

from django.db import models

class User(models.Model) : 
    name = models.CharField(max_length = 140)
    pw = models.CharField(max_length = 20)
    email = models.CharField(max_length = 50)
    role = models.CharField(max_length = 10)
    expert = models.BooleanField(default=False)
    
    def __str__(self) :
        return self.name
        
class Topic(models.Model):
    topic = models.CharField(max_length = 200)
    date = models.DateTimeField()
    
    def __str__(self) :
        return self.topic
        
class Dataset(models.Model) :
    topic_id =  models.ForeignKey('Topic',on_delete=models.CASCADE,)
    title = models.TextField()
    content = models.TextField()
    
    def __str__(self) :
        return self.title
    

class Curation(models.Model):
    topic_id = models.ForeignKey('Topic',on_delete=models.CASCADE,)
    data_id = models.ForeignKey('Dataset', on_delete = models.CASCADE,)
    user_id = models.ForeignKey('User', on_delete = models.CASCADE,) 
    result = models.BooleanField(default = False)
    comment = models.TextField(default=None)
    submit = models.BooleanField(default = False)
    def __str__(self):
        return self.comment
    
class Summary(models.Model):
    topic_id = models.ForeignKey('Topic',on_delete=models.CASCADE)
    finalresult = models.BooleanField(default = False)
    

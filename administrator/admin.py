from django.contrib import admin
from administrator.models import  Topic, Curation, Dataset, Summary
from django.contrib.auth.models import User
# Register your models here.
# admin.site.register(User)
admin.site.register(Curation)
admin.site.register(Dataset)
admin.site.register(Summary)
admin.site.register(Topic)
# Register your models here.

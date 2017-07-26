from django import forms
from administrator.models import  User, Topic, Curation, Dataset, Summary
from django.forms.widgets import TextInput

class CurationFrom(forms.ModelForm):
    class Meta:
        model = Curation
        fields = [
                "result",
                "comment",
        ]
        widgets = {
   
            'result':forms.RadioSelect(attrs={'type': 'radio', 'name':'selector'}),
            #'result':forms.RadioSelect(attrs={'class':"radio-inline"}),
            'comment': forms.Textarea(attrs={'row': 10,'style':'top: 10px; position: relative','placeholder':'leave your comment'}),
           
            
        }
       

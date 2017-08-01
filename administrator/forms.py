
from django.forms import EmailField
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

    
class UserRegisterForm(UserCreationForm):
    email = EmailField(label = 'Email address',help_text=_("Required, but never shown."))
    class Meta:
        model = User
        fields = [
            'username' ,
            'email',
            'password1',
            'password2'
        ]
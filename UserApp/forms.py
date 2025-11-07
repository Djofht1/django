
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
   class Meta:
        model=User
        fields=['username','first_name','email','password1','password2']  
        widgets={
                "email":forms.EmailInput(),
                "password1":forms.PasswordInput()
        }



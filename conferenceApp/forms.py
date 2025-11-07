from django import forms
from .models import conference
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ConferenceModel(forms.ModelForm):
    class Meta:
        model=conference
        fields=['name','location','start_date','end_date','Description','theme']
        labels={
            'name':'Nom de la conference',
            'location':'Lieu de la conference',
            'start_date':'Date de debut',
            'end_date':'Date de fin',
            'Description':'Description',
            'theme':'Themes',
        }
        widgets={
            'start_date':forms.DateInput(attrs={'placeholder':'date de debuit','type':'date'}),
            'end_date':forms.DateInput(attrs={'placeholder':'date fin','type':'date'}),
            
        }



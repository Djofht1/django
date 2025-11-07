from django.shortcuts import render
from .models import conference 
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from  django.urls import reverse_lazy 
from .forms import ConferenceModel
from django.contrib.auth.mixins import LoginRequiredMixin  

def all_conferneces(request):
    conferences=conference.objects.all()
    return render(request,"conference/liste_conferences.html",{"liste":conferences})    

# Create your views here.
class Conferencelist(ListView):
    model=conference
    context_object_name="liste"
    ordering =["start_date"]
    template_name="conference/liste_conferences.html"

class ConferenceDetails(DetailView):
    model=conference
    template_name="conference/detail.html"
    context_object_name="conference"    

class ConferenceCreate(LoginRequiredMixin,CreateView):
    model=conference
    template_name="conference/conference_form.html"
    #fields="__all__"
    form_class=ConferenceModel
    success_url = reverse_lazy("liste_conferences")

class ConferenceUpdate(LoginRequiredMixin,UpdateView):
    model=conference
    template_name="conference/conference_form.html"
    #fields="__all__"
    form_class=ConferenceModel
    success_url = reverse_lazy("liste_conferences")

class ConferenceDelete(LoginRequiredMixin,DeleteView):
    model=conference
    template_name="conference/conference_confirm_delete.html"
    success_url = reverse_lazy("liste_conferences")



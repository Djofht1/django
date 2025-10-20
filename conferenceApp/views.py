from django.shortcuts import render
from .models import conference 
from django.views.generic import ListView,DetailView    
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

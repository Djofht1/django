from django.shortcuts import render
from .models import conference 
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from  django.urls import reverse_lazy 
from .forms import ConferenceModel
from django.contrib.auth.mixins import LoginRequiredMixin  
from .models import submission
from .forms import SubmissionForm, SubmissionUpdateForm
from django.utils import timezone
from django.core.exceptions import PermissionDenied

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


# Liste des soumissions pour l'utilisateur connecté
class ListSubmissionsView(LoginRequiredMixin, ListView):
    model = submission
    template_name = 'conferenceApp/submission_list.html'
    context_object_name = 'submissions'
    login_url = '/user/login/'

    def get_queryset(self):
        return submission.objects.filter(user=self.request.user).order_by('-submission_date')


# Détail d’une soumission
class DetailSubmissionView(LoginRequiredMixin, DetailView):
    model = submission
    template_name = 'conferenceApp/submission_detail.html'
    context_object_name = 'submission'
    pk_url_kwarg = 'submission_id'
    login_url = '/user/login/'

class SubmissionCreateView(LoginRequiredMixin, CreateView):
    model = submission
    form_class = SubmissionForm
    template_name = 'conferenceApp/submission_form.html'
    success_url = reverse_lazy('list_submissions')
    login_url = '/user/login/'
    # Cela permet d’avoir le champ conference déjà rempli dans le formulaire, selon l’ID présent dans l’URL.
    def get_initial(self):
        """Pré-remplir le champ conférence si présent dans l’URL"""
        initial = super().get_initial()# récupère les valeurs par défaut
        conference_id = self.kwargs.get('conference_id') # lit l'ID dans l'URL
        if conference_id:
            initial['conference'] = conference.objects.get(pk=conference_id)# charge l'objet conférence
        return initial

    def form_valid(self, form):
        # Associer automatiquement l’utilisateur connecté
        form.instance.user = self.request.user

        # Associer la conférence via l’URL
        conference_id = self.kwargs.get('conference_id')
        if conference_id:
            form.instance.conference = conference.objects.get(pk=conference_id)
        else:
            form.add_error(None, "Aucune conférence sélectionnée.")
            return self.form_invalid(form)   # Si erreur, ne sauvegarde pas

        return super().form_valid(form) # 🔹 Continue le traitement normal


class SubmissionUpdateView(LoginRequiredMixin, UpdateView):
    model = submission 
    form_class = SubmissionUpdateForm
    template_name = 'conferenceApp/submission_form.html'
    success_url = reverse_lazy('list_submissions')
    login_url = '/user/login/'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object() # récupère la soumission actuelle

        if obj.user != request.user:
            raise PermissionDenied("Vous n'êtes pas autorisé à modifier cette soumission.")
        if obj.status in ['accepted', 'rejected']:
            raise PermissionDenied("Cette soumission ne peut plus être modifiée.")
        return super().dispatch(request, *args, **kwargs)

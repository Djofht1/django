from django.urls import path,include
from . import views
from .views import *


urlpatterns = [
   # path('liste/',views.all_conferneces,name="liste_conferences"),
    path("liste/",Conferencelist.as_view(),name="liste_conferences"),
   # path("Conferenece_details/<int:pk>/",ConferenceDetails.as_view(),name="conference_details")
    path('conference/<int:pk>/',ConferenceDetails.as_view(),name='conference_details')
]
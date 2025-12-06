from django.urls import path,include
from . import views
from .views import *
from .views import ListSubmissionsView, DetailSubmissionView, SubmissionCreateView

urlpatterns = [
   # path('liste/',views.all_conferneces,name="liste_conferences"),
    path("liste/",Conferencelist.as_view(),name="liste_conferences"),
   # path("Conferenece_details/<int:pk>/",ConferenceDetails.as_view(),name="conference_details")
    path('conference/<int:pk>/',ConferenceDetails.as_view(),name='conference_details'),
     path("form/",ConferenceCreate.as_view(),name="confrerence_add"),
     path("<int:pk>/update/",ConferenceUpdate.as_view(),name="conference_update"),
     path("<int:pk>/delete/",ConferenceDelete.as_view(),name="conference_delete"),
      path('submissions/', ListSubmissionsView.as_view(), name='list_submissions'),
      path('submission/add/', SubmissionCreateView.as_view(), name='submission_add'),
      path('submission/<str:submission_id>/', DetailSubmissionView.as_view(), name='detail_submission'),
       path('submission/<int:pk>/update/', SubmissionUpdateView.as_view(), name='submission_update'),
       path('submission/add/<int:conference_id>/', SubmissionCreateView.as_view(), name='submission_add'),


]
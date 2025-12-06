from rest_framework import serializers
from SessionApp.models import Session  # importe ton modèle

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'  # tous les champs du modèle

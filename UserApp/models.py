from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

import uuid 
# Create your models here.
def generer_user_id():
    return "USER"+uuid.uuid4().hex[:4].upper()
def verify_email(email):
    domaine=["esprit.tn","sesame.com","tekup.tn"]
    if email.split("@")[1] not  in domaine:
        raise ValidationError("l'email est invalid et doit appartenir a esprit.tn, sesame.com ou tekup.tn")
    
name_validator=RegexValidator(r'^[a-zA-Z]+$', 'Only alphabetic characters are allowed.')

class User(AbstractUser):
    user_id=models.CharField(max_length=8,primary_key=True,unique=True,editable=False) 
    first_name=models.CharField(max_length=255,validators=[name_validator])
    last_name=models.CharField(max_length=255,validators=[name_validator])
    email=models.EmailField(unique=True, validators=[verify_email])
    affiliation=models.CharField(max_length=55)
    nationality=models.CharField(max_length=255)
    ROLE=[("participant","participant"),("commite","organizing commitee member")]
    role=models.CharField(max_length=100,choices=ROLE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def save(self,*args,**kwargs):
        if not self.user_id:
            new_id = generer_user_id()
            while User.objects.filter(user_id=new_id).exists():  # ✅ correction ici
                    new_id = generer_user_id()
            self.user_id = new_id
        super().save(*args,**kwargs)
       
class OrganizingComitee(models.Model):
    user=models.ForeignKey("UserApp.User", on_delete=models.CASCADE,related_name="committee")
    conference=models.ForeignKey("conferenceApp.conference", on_delete=models.CASCADE,related_name="committee")
    ROLES=[("chair","chair"),
           ("co_chair","co_chair"),
           ("member","member")
           ]
    commitee_role=models.CharField(max_length=255,choices=ROLES)
    date_join=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    # submission=models.ManyToManyField("conferenceApp.submission",through='submission')
   # OrganizingComiteelist=models.ManyToManyField("conferenceApp.conference",through='OrganizingComitee')

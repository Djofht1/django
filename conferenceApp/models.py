from django.db import models
from django.core.validators import MinLengthValidator ,RegexValidator ,FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class conference(models.Model):
    conference_id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zÀ-ÿ\s\-]+$',
                message="Le nom de la conférence ne doit contenir que des lettres."
            )
        ]
    )
    Description = models.TextField(
        max_length=255,
        validators=[MinLengthValidator(30, "La description doit contenir au moins 30 caractères.")]
    )
    location = models.CharField(max_length=255)
    THEME_CHOICES = [
        ("cs&ia", "Computer Science & IA"),
        ("cs", "Social Science"),
        ("SE", "Science and Engineering")
    ]
    theme = models.CharField(max_length=255, choices=THEME_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("La date de fin doit être après la date de début.")

    def duration(self):
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            return delta.days
        return 0
    
    def __str__(self):
        return self.name

            
    def duration(self):
        # Return number of days safely
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            return delta.days
        return 0 
class submission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    user = models.ForeignKey("UserApp.User", on_delete=models.CASCADE, related_name="submission")
    conference = models.ForeignKey("conferenceApp.conference", on_delete=models.CASCADE, related_name="submission")
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    keywords = models.TextField()
    paper = models.FileField(
        upload_to="paper/",
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="Le fichier doit être au format PDF uniquement."
    )
    CHOICES = [
        ("submitted", "submitted"),
        ("under review", "under review"),
        ("accepted", "accepted"),
        ("rejected", "rejected")
    ]
    status = models.CharField(max_length=255, choices=CHOICES)
    payed = models.BooleanField(default=False)
    submission_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"








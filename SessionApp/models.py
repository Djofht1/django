from django.db import models
from django.core.exceptions import ValidationError

class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    session_day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    conference = models.ForeignKey("conferenceApp.conference", on_delete=models.CASCADE, related_name="session")

    def clean(self):
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError("End time must be after start time")

    def duration(self):
        """Return the duration in minutes."""
        if self.start_time and self.end_time:
            delta = (self.end_time.hour * 60 + self.end_time.minute) - (self.start_time.hour * 60 + self.start_time.minute)
            return delta
        return 0

    def __str__(self):
        return f"{self.title} - {self.topic}"

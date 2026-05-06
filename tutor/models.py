from django.db import models
from django.conf import settings

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class TutorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tutor_profile')
    bio = models.TextField(blank=True, null=True)
    availability = models.CharField(max_length=200, blank=True, null=True, help_text="E.g., Mon-Fri 10AM-4PM")
    is_approved = models.BooleanField(default=False)
    subjects = models.ManyToManyField(Subject, blank=True)
    rejection_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

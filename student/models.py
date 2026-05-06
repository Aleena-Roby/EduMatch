from django.db import models
from django.conf import settings

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    grade_level = models.CharField(max_length=50, blank=True, null=True)
    fee_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

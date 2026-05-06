from django.db import models
from django.conf import settings
from tutor.models import Subject

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )
    PAYMENT_CHOICES = (
        ('cash', 'Cash'),
        ('upi', 'UPI (Google Pay / PhonePe / Paytm)'),
        ('card', 'Credit / Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('free', 'Free Session'),
    )
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_bookings')
    tutor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tutor_bookings')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    session_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash')
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} with {self.tutor.username} on {self.session_date}"

class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_reviews')
    tutor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} stars for {self.tutor.username} by {self.student.username}"

from django.contrib import admin
from .models import Booking, Review

class BookingAdmin(admin.ModelAdmin):
    list_display = ('student', 'tutor', 'subject', 'session_date', 'payment_type', 'status')
    list_filter = ('status', 'payment_type', 'session_date')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('student', 'tutor', 'rating', 'created_at')
    list_filter = ('rating',)

admin.site.register(Booking, BookingAdmin)
admin.site.register(Review, ReviewAdmin)

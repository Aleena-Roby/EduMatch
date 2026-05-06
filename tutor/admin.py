from django.contrib import admin
from .models import TutorProfile, Subject

@admin.action(description='Approve selected tutors')
def approve_tutors(modeladmin, request, queryset):
    queryset.update(is_approved=True)

class TutorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_approved', 'availability')
    list_filter = ('is_approved',)
    actions = [approve_tutors]

admin.site.register(TutorProfile, TutorProfileAdmin)
admin.site.register(Subject)

"""
URL configuration for edumatch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "EduMatch Administration"
admin.site.site_title = "EduMatch Admin Portal"
admin.site.index_title = "Welcome to EduMatch Admin Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('student/', include('student.urls')),
    path('tutor/', include('tutor.urls')),
]

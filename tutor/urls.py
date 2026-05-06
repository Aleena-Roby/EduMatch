from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.tutor_dashboard, name='tutor_dashboard'),
    path('booking/<int:booking_id>/<str:action>/', views.handle_booking, name='handle_booking'),
    path('profile/edit/', views.edit_tutor_profile, name='edit_tutor_profile'),
]

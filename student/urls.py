from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('tutors/', views.tutor_list, name='tutor_list'),
    path('book/<int:tutor_id>/', views.book_tutor, name='book_tutor'),
]

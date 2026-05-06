from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/student/', views.student_register, name='student_register'),
    path('register/tutor/', views.tutor_register, name='tutor_register'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/approve-tutor/<int:tutor_id>/', views.approve_tutor, name='approve_tutor'),
    path('dashboard/toggle-fee/<int:student_id>/', views.toggle_fee, name='toggle_fee'),
    path('dashboard/add-subject/', views.add_subject, name='add_subject'),
    path('dashboard/update-subject-price/<int:subject_id>/', views.update_subject_price, name='update_subject_price'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('dashboard/reject-tutor/<int:tutor_id>/', views.reject_tutor, name='reject_tutor'),
    path('dashboard/delete-tutor/<int:tutor_id>/', views.delete_tutor, name='delete_tutor'),
]

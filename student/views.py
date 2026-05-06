from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from tutor.models import TutorProfile, Subject
from booking.models import Booking
from django.contrib import messages
from datetime import datetime

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('landing_page')
    bookings = Booking.objects.filter(student=request.user).order_by('-session_date')
    return render(request, 'student_dashboard.html', {'bookings': bookings})

@login_required
def tutor_list(request):
    if request.user.role != 'student':
        return redirect('landing_page')
    
    tutors = TutorProfile.objects.filter(is_approved=True)
    subjects = Subject.objects.all()
    
    subject_id = request.GET.get('subject')
    if subject_id:
        tutors = tutors.filter(subjects__id=subject_id)
        
    return render(request, 'tutor_list.html', {'tutors': tutors, 'subjects': subjects, 'selected_subject': subject_id})

@login_required
def book_tutor(request, tutor_id):
    if request.user.role != 'student':
        return redirect('landing_page')
        
    tutor_profile = get_object_or_404(TutorProfile, id=tutor_id, is_approved=True)
    
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        session_date_str = request.POST.get('session_date')
        message = request.POST.get('message')
        payment_type = request.POST.get('payment_type', 'cash')

        if subject_id and session_date_str:
            subject = get_object_or_404(Subject, id=subject_id)
            try:
                session_date = datetime.strptime(session_date_str, '%Y-%m-%dT%H:%M')
                Booking.objects.create(
                    student=request.user,
                    tutor=tutor_profile.user,
                    subject=subject,
                    session_date=session_date,
                    payment_type=payment_type,
                    message=message
                )
                messages.success(request, 'Booking request sent successfully!')
                return redirect('student_dashboard')
            except ValueError:
                messages.error(request, 'Invalid date format.')
        else:
            messages.error(request, 'Please select a subject and session date.')
            
    return render(request, 'book_tutor.html', {'tutor_profile': tutor_profile})

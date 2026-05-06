from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TutorProfile, Subject
from booking.models import Booking
from django.contrib import messages

@login_required
def tutor_dashboard(request):
    if request.user.role != 'tutor':
        return redirect('dashboard')
    bookings = Booking.objects.filter(tutor=request.user).order_by('-created_at')
    return render(request, 'tutor_dashboard.html', {'bookings': bookings})

@login_required
def handle_booking(request, booking_id, action):
    if request.user.role != 'tutor':
        return redirect('landing_page')
        
    booking = get_object_or_404(Booking, id=booking_id, tutor=request.user)
    
    if action == 'accept':
        booking.status = 'accepted'
        messages.success(request, 'Booking accepted.')
    elif action == 'reject':
        booking.status = 'rejected'
        messages.success(request, 'Booking rejected.')
        
    booking.save()
    return redirect('tutor_dashboard')

@login_required
def edit_tutor_profile(request):
    if request.user.role != 'tutor':
        return redirect('landing_page')
        
    profile = request.user.tutor_profile
    subjects = Subject.objects.all()
    
    if request.method == 'POST':
        profile.bio = request.POST.get('bio')
        profile.availability = request.POST.get('availability')
        
        # update subjects
        subject_ids = request.POST.getlist('subjects')
        if subject_ids:
            profile.subjects.set(subject_ids)
        else:
            profile.subjects.clear()
            
        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('tutor_dashboard')
        
    return render(request, 'edit_tutor_profile.html', {
        'profile': profile,
        'subjects': subjects,
        'selected_subjects': profile.subjects.values_list('id', flat=True)
    })

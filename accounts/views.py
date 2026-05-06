from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from student.models import StudentProfile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import StudentRegistrationForm, TutorRegistrationForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from tutor.models import TutorProfile
from booking.models import Booking
from .models import User
from django.contrib import messages

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')

def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'student_register.html', {'form': form})

def tutor_register(request):
    if request.method == 'POST':
        form = TutorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = TutorRegistrationForm()
    return render(request, 'tutor_register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard_redirect(request):
    if request.user.is_superuser or request.user.role == 'admin':
        return redirect('admin_dashboard')
    elif request.user.role == 'tutor':
        return redirect('tutor_dashboard')
    elif request.user.role == 'student':
        return redirect('student_dashboard')
    
    # If authenticated but no role assigned, just show the landing page
    # to avoid redirection loops between landing_page and dashboard_redirect
    return render(request, 'index.html')

@login_required
def admin_dashboard(request):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('dashboard')

    tutors = TutorProfile.objects.all().order_by('-user__date_joined')
    student_profiles = StudentProfile.objects.select_related('user').order_by('-user__date_joined')
    total_bookings = Booking.objects.count()
    pending_tutors_qty = TutorProfile.objects.filter(is_approved=False).count()

    from tutor.models import Subject
    subjects = Subject.objects.all()

    context = {
        'tutors': tutors,
        'student_profiles': student_profiles,
        'students_count': student_profiles.count(),
        'bookings_count': total_bookings,
        'pending_tutors': pending_tutors_qty,
        'total_tutors': tutors.count(),
        'subjects': subjects
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def approve_tutor(request, tutor_id):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('dashboard')
        
    tutor = get_object_or_404(TutorProfile, id=tutor_id)
    tutor.is_approved = True
    tutor.rejection_reason = None
    tutor.save()
    messages.success(request, f"Tutor {tutor.user.username} approved successfully.")
    return redirect('admin_dashboard')

@login_required
def toggle_fee(request, student_id):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('dashboard')
    profile = get_object_or_404(StudentProfile, id=student_id)
    profile.fee_paid = not profile.fee_paid
    profile.save()
    status = 'Paid' if profile.fee_paid else 'Unpaid'
    messages.success(request, f"{profile.user.username}'s fee marked as {status}.")
    return redirect('admin_dashboard')

@login_required
def add_subject(request):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('dashboard')
    
    if request.method == 'POST':
        from tutor.models import Subject
        name = request.POST.get('name')
        description = request.POST.get('description')
        price_str = request.POST.get('price')
        
        if name and price_str:
            try:
                price = float(price_str)
                Subject.objects.create(name=name, description=description, price=price)
                messages.success(request, f"Successfully added '{name}' to the marketplace.")
            except ValueError:
                messages.error(request, "Invalid price format. Please enter a number.")
        else:
            messages.error(request, "Subject name and price are required.")
            
    return redirect('admin_dashboard')

@login_required
def update_subject_price(request, subject_id):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('dashboard')
    
    from tutor.models import Subject
    subject = get_object_or_404(Subject, id=subject_id)
    
    if request.method == 'POST':
        new_price = request.POST.get('price')
        if new_price:
            subject.price = new_price
            subject.save()
            messages.success(request, f"Price for {subject.name} updated successfully.")
        else:
            messages.error(request, "Invalid price value.")
            
    return redirect('admin_dashboard')

def forgot_password(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(username=username, email=email)
                request.session['reset_user_id'] = user.id
                return redirect('reset_password')
            except User.DoesNotExist:
                messages.error(request, "Username and Email do not match our records.")
    else:
        form = ForgotPasswordForm()
            
    return render(request, 'forgot_password.html', {'form': form})

def reset_password(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('forgot_password')
        
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            del request.session['reset_user_id']
            messages.success(request, "Password reset successful! You can now login.")
            return redirect('login')
    else:
        form = ResetPasswordForm()
            
    return render(request, 'reset_password.html', {'reset_user': user, 'form': form})

@login_required
def reject_tutor(request, tutor_id):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('dashboard')
        
    tutor = get_object_or_404(TutorProfile, id=tutor_id)
    tutor.is_approved = False
    
    reason = request.POST.get('reason')
    if not reason:
        reason = "Your application requires further review. Please ensure your bio and expertise are accurately described."
    
    tutor.rejection_reason = reason
    tutor.save()
    messages.warning(request, f"Tutor {tutor.user.username}'s application has been updated to 'Rejected' status.")
    return redirect('admin_dashboard')

@login_required
def delete_tutor(request, tutor_id):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('dashboard')
        
    tutor_profile = get_object_or_404(TutorProfile, id=tutor_id)
    user_to_delete = tutor_profile.user
    username = user_to_delete.username
    
    # Deleting the user will CASCADE delete the TutorProfile and all their Bookings
    user_to_delete.delete()
    
    messages.success(request, f"Tutor {username}, their profile, and all associated requests have been permanently removed.")
    return redirect('admin_dashboard')

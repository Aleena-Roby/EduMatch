from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from student.models import StudentProfile
from tutor.models import TutorProfile, Subject

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
        help_text="Required. Valid email address."
    )
    grade_level = forms.CharField(
        max_length=50, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Grade 10, Freshman...'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'grade_level')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Choose a unique username'})
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({'placeholder': 'Create a strong password'})
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm your password'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        if commit:
            user.save()
            StudentProfile.objects.create(user=user, grade_level=self.cleaned_data.get('grade_level'))
        return user

class SubjectMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name} (₹{obj.price}/session)"

class TutorRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'placeholder': 'yourname@example.com'}),
        help_text="Required for verification and account recovery."
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell students about your teaching style and experience...'}), 
        required=False, 
        label="Bio / Introduction"
    )
    availability = forms.CharField(
        max_length=200, 
        required=False, 
        help_text="E.g., Mon-Fri 10AM-4PM", 
        label="Availability",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Weekdays 6pm - 9pm'})
    )
    subjects = SubjectMultipleChoiceField(
        queryset=Subject.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Subjects You Teach"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'bio', 'availability', 'subjects')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Tutor username'})
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({'placeholder': 'Create a strong password'})
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm your password'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'tutor'
        if commit:
            user.save()
            profile = TutorProfile.objects.create(
                user=user,
                bio=self.cleaned_data.get('bio'),
                availability=self.cleaned_data.get('availability')
            )
            selected_subjects = self.cleaned_data.get('subjects')
            if selected_subjects:
                profile.subjects.set(selected_subjects)
        return user

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Registered email address'}))

class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'New password'}),
        label="New Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}),
        label="Confirm Password"
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

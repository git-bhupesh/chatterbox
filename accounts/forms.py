from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

# --- Signup Form ---
class CustomSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    dob = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date of Birth"
    )

    class Meta:
        model = User
        # UserCreationForm handles password fields automatically, 
        # so we just need the identity fields here.
        fields = ['username', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        # 1. Save the User object
        user = super().save(commit=commit)
        
        # 2. Update the profile with the extra fields
        # Note: The profile is already created by your signals.py
        if commit:
            user.profile.dob = self.cleaned_data.get('dob')
            user.profile.save()
        return user


# --- Profile Editing Forms ---

class UserForm(forms.ModelForm):
    """Handles core identity fields."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserProfileForm(forms.ModelForm):
    """Handles the customizable parts of the profile."""
    class Meta:
        model = UserProfile
        fields = ['dob', 'bio', 'avatar']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }
        
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input-styled'})
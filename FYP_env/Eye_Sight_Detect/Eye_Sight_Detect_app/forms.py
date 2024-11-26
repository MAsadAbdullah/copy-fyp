from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'phone', 'license_no', 'specialty', 'start_year', 'clinic_address', 'country', 'password1', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
            'license_no': forms.TextInput(attrs={'placeholder': 'Enter your license number'}),
            'specialty': forms.TextInput(attrs={'placeholder': 'Enter your specialty'}),
            'start_year': forms.NumberInput(attrs={'placeholder': 'Enter your start year'}),
            'clinic_address': forms.TextInput(attrs={'placeholder': 'Enter your clinic address'}),
            'country': forms.TextInput(attrs={'placeholder': 'Enter your country'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter your password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm your password'})

class CustomUserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))


Gender = (
    ('', 'Choose...'),
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),)
class PatientForm(forms.ModelForm):
    def set_request(self, request):
        self.request = request
    class Meta:
        model = Patient
        fields = '__all__'
        exclude = ['added_by_id', 'arival_date_time']
        
    name=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    phone=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Phone'}))
    cnic=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'CNIC'}))
    is_minor = forms.BooleanField(required=False,label='Check this box if patient is a child')
    gender = forms.ChoiceField(choices=Gender,required=True)
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'City'}))
    
    previous_medical_history = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4,'placeholder': 'if any'}),
        label='Previous Medical History'
    )
    allergies = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4,'placeholder': 'if any'}),
        label='Allergies'
    )
    family_medical_history = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4,'placeholder': 'if any'}),
        label='Family Medical History'
    )
    # left_eye_fundus_image = forms.FileField(label='Attach Left Eye Fundus Image')
    # right_eye_fundus_image = forms.FileField(label='Attach Right Eye Fundus Image')
    image_metadata = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4,'placeholder': 'Equipment used, etc.'}),
        label='Image Metadata'
    )
    doctor_remarks = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4,'placeholder': 'if any'}),
        label='Doctor`s Remarks'
    )
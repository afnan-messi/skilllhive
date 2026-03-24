from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control rounded-pill bg-dark text-white border-secondary', 'placeholder': 'Email'}))
    
    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control rounded-pill bg-dark text-white border-secondary', 'placeholder': 'Username'}),
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].widget.attrs.update({
                'class': 'form-control rounded-pill bg-dark text-white border-secondary',
                'placeholder': 'Password' if fieldname == 'password1' else 'Confirm Password'
            })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'profile_picture', 'banner_image']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'banner_image': forms.FileInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
        }

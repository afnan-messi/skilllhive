from django import forms
from .models import UserSkill

class UserSkillForm(forms.ModelForm):
    class Meta:
        model = UserSkill
        fields = ['skill_name', 'skill_type', 'category', 'level', 'description', 'demo_file', 'availability']
        widgets = {
            'skill_name': forms.TextInput(attrs={
                'class': 'form-control rounded-pill bg-dark text-white border-secondary',
                'placeholder': 'Enter skill name'
            }),
            'skill_type': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select rounded-pill bg-dark text-white border-secondary'
            }),
            'level': forms.Select(attrs={
                'class': 'form-select rounded-pill bg-dark text-white border-secondary'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control rounded-4 bg-dark text-white border-secondary',
                'rows': 4,
                'placeholder': 'Describe what you want to teach or learn...'
            }),
            'demo_file': forms.FileInput(attrs={
                'class': 'form-control rounded-pill bg-dark text-white border-secondary'
            }),
            'availability': forms.TextInput(attrs={
                'class': 'form-control rounded-pill bg-dark text-white border-secondary',
                'placeholder': 'e.g. Mon-Fri, 6 PM - 8 PM'
            }),
        }

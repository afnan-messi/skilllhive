from django import forms
from .models import ResearchPaper, PaperReview, Discussion

class ResearchPaperForm(forms.ModelForm):
    class Meta:
        model = ResearchPaper
        fields = ['title', 'abstract', 'category', 'paper_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control rounded-pill bg-dark text-white border-secondary', 'placeholder': 'Paper Title'}),
            'abstract': forms.Textarea(attrs={'class': 'form-control rounded-4 bg-dark text-white border-secondary', 'placeholder': 'Abstract', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select rounded-pill bg-dark text-white border-secondary'}),
            'paper_file': forms.FileInput(attrs={'class': 'form-control rounded-pill bg-dark text-white border-secondary'}),
        }

class PaperReviewForm(forms.ModelForm):
    class Meta:
        model = PaperReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select rounded-pill bg-dark text-white border-secondary'}),
            'comment': forms.Textarea(attrs={'class': 'form-control rounded-4 bg-dark text-white border-secondary', 'placeholder': 'Your review...', 'rows': 3}),
        }

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control rounded-4 bg-dark text-white border-secondary', 'placeholder': 'Start a discussion...', 'rows': 2}),
        }

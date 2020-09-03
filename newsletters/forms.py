from django import forms

from .models import NewsletterUser

class NewsletterUserSignUp(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Newsletter Email'}), required=True, max_length=255)

    class Meta:
        model = NewsletterUser
        fields = (
            'email',
        )
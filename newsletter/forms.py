from django import forms
from .models import NewsletterUser


class NewsletterSignUpForm(forms.ModelForm):
    class Meta:
        model= NewsletterUser
        fields = (
            'email',
        )

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            my = validate_email(email)
        except:
            return forms.ValidationError("Email incorrect")
        return email

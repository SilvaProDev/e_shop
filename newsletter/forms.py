from django import forms
from .models import NewsletterUser


class NewsletterSignUpForm(forms.Form):
    email  = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email for the newsletter'}), required=True, max_length=255)
    class Meta:
        model= NewsletterUser
        fields = (
            'email',
        )

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     try:
    #         my = validate_email(email)
    #     except:
    #         return forms.ValidationError("Email incorrect")
    #     return email

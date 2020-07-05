from django import forms 
from .models import ContactMessage

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name'}), required=True, max_length=30)
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}), required=True, max_length=100)
    subject = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Subject'}), required=True, max_length=50)
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Your Message', 'rows':'5'}), required=True, max_length=255)

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)
    catid = forms.IntegerField()


from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
from .models import Newsletter, NewsletterUser
from .forms import NewsletterSignUpForm
from product.models import Category

def newsletter(request):
    if request.method=='POST':
        form = NewsletterSignUpForm(request.POST)
        if form.is_valid():
            instance = NewsletterUser()
            instance.email = form.cleaned_data['email']
            instance.save()
            newsletter = Newsletter.objects.get(id=instance.id)
            if newsletter.status==True:
                subject = newsletter.subject
                body = newsletter.body
                from_email = settings.EMAIL_HOST_USER
                for email in newsletter.email.all():
                    send_mail(subject=subject, from_email=from_email, recipient_list=[email], message=body, fail_silently=True)

    form =NewsletterSignUpForm()
    categorie = Category.objects.all()

    context = {
        "form":form,
        "categorie":categorie,
    }
    return render(request, 'pages/index.html', context)



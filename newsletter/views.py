from django.shortcuts import render

# Create your views here.
# from .models import Newsletter
# from .forms import NewsletterSignUpForm

# def newsletter(request):
#     form = NewsletterSignUpForm(request.POST)

#     if form.is_valid():
#         instance = form.save()
#         newsletter = Newsletter.objects.get(id=instance.id)
#         if newsletter.status==True:
#             subject = newsletter.subject
#             body = newsletter.body
#             from_email = settings.EMAIL_HOST_USER
#             for email in newsletter.email.all():
#                 send_mail(subject=subject, from_email=from_email, recipient_list=[email], message=body, fail_silently=True)
from django.urls import path

from . import views

#uapp_name="newsletter"

urlpatterns = [
    path('newsletterUser/',views.newsletter, name="newsletterUser")
	
]
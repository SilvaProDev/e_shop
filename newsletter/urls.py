from django.urls import path

from . import views

urlpatterns = [
    path('newsletterUser/',views.newsletter, name="newsletterUser")
	
]
from django.db import models

# Create your models here.


class NewsletterUser(models.Model):
    email = models.EmailField(max_length=255)
    status = models.BooleanField(default=True)

    date_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name= "Newsletter User"
        verbose_name_plural="Newsletter Users"

    def __str__(self):
        return self.email

class Newsletters(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    emails = models.ManyToManyField(NewsletterUser)
    status = models.BooleanField(default=True)

    date_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Newsletter"
        verbose_name_plural = "Newsletters messages"

    def __str__(self):
        return self.subject

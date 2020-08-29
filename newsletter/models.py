from django.db import models

# Create your models here.

class NewsletterUser(models.Model):
    email = models.EmailField()
    date_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name="Newsletter"
        verbose_name_plural="Newsletters User"

    def __str__(self):
        return self.email


class Newsletter(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    email = models.ForeignKey(NewsletterUser, on_delete=models.CASCADE, related_name='newsletter')
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)

    date_mod = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name ="Newsletter"
        verbose_name_plural = "Newsletter Messages"

    def __str__(self):
        return self.subject


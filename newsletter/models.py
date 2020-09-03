from django.db import models

# Create your models here.

class NewsletterUser(models.Model):
    email = models.EmailField(max_length=255)
    date_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name="Newsletter"
        verbose_name_plural="Newsletters User"

    def __str__(self):
        return self.email


class Newsletter(models.Model):
    # STATUS = (
    #     ('True', 'True'),
    #     ('False', 'False'),
    #     ('Publie', 'Publie')
    # )
    subject = models.CharField(max_length=255)
    body = models.TextField()
    email = models.ManyToManyField(NewsletterUser)
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)

    date_mod = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name ="Newsletter"
        verbose_name_plural = "Newsletter Messages"

    def __str__(self):
        return self.subject


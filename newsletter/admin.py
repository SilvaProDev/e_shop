from django.contrib import admin

# Register your models here.
from newsletter.models import NewsletterUser, Newsletter

class NewsletterUserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'date_add',
    )

class NewsletterAdmin(admin.ModelAdmin):
    list_display = (
        'subject',
        'date_add',
        'status',
        
    )

admin.site.register(NewsletterUser, NewsletterUserAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
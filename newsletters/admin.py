from django.contrib import admin

# Register your models here.
from .models import NewsletterUser, Newsletters

class NewsletterUserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'status',
        'date_add',
    )
    list_filter = (
        'status',
        'date_add',
    )
class NewslettersAdmin(admin.ModelAdmin):
    list_display = (
        'subject',
        'status',
        'date_add',
    )
    list_filter = (
        'status',
        'date_add',
    )

admin.site.register(NewsletterUser, NewsletterUserAdmin)
admin.site.register(Newsletters, NewslettersAdmin)

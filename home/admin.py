from django.contrib import admin
from  home.models import Setting, ContactMessage, Faq
# Register your models here.
class SettingAdmin(admin.ModelAdmin):
    list_display = ['titre', 'company', 'date_add', 'status']
    
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'status',]
    list_filter = ['status']
    readonly_fields = (
        'name',
        'email',
        'subject',
        'message',
        'ip',
    )
    
class FaqAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'ordernumber','status']
    list_filter = ['status']
    

admin.site.register(Setting, SettingAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(Faq, FaqAdmin)
from django.contrib import admin
from  home.models import Setting, ContactMessage, Faq, Language, SettingLang
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

class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'code','status']
    list_filter = ['status']

class SettingLangAdmin(admin.ModelAdmin):
    list_display = ['titre', 'keyword','description', 'lang']
    list_filter = ['lang']


    

admin.site.register(Setting, SettingAdmin)
admin.site.register(SettingLang, SettingLangAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(Faq, FaqAdmin)
admin.site.register(Language, LanguageAdmin)
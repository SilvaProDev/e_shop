from django.contrib import admin
from .models import ShopCart, Order, OrderProduit
# Register your models here.

class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['produit','user','quantity','price','amount',]
        
    list_filter = ['produit',]

class OrderProduitline(admin.TabularInline):
    model = OrderProduit
    readonly_fields = ('user','produit','price','quantity','amount',)
    can_delete=False
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','phone','city','total','status',]
    list_filter = ['status',]
    readonly_fields = ('user','address','city','country','phone', 'code','first_name','last_name','ip','total')
    can_delete=False
    inlines = [OrderProduitline]
        
class OrderProduitAdmin(admin.ModelAdmin):
    list_display = ['user','produit','price','quantity','amount']
    list_filter = ['user',]
    


admin.site.register(ShopCart, ShopCartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduit, OrderProduitAdmin)
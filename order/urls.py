from django.urls import path

from .import views
app_name = 'order'
urlpatterns = [
	
   path('', views.index, name="index"),
   path('add-to-shop-cart/<int:id>', views.add_to_shop_cart, name="add-to-shop-cart"),
   path('delete-from-shop-cart/<int:id>', views.delete_to_shop_cart, name="delete-from-shop-cart"),
   path('orderproduit/', views.orderproduit, name="orderproduit"),
]


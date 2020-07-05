from django.urls import path, include

from . import views

urlpatterns = [
	path('', views.index, name = 'home'),
	path('about-us/', views.aboutus, name = 'about_us'),
	path('contact-us/', views.contactus, name = 'contact-us'),
	path('categorie/<int:id>/<slug:slug>', views.product_categorie, name = 'product_categorie'),
	path('search/', views.search, name = 'search'),
	path('shop-cart/', views.shop_cart, name = 'shop-cart'),
	path('search_auto/', views.search_auto, name = 'search_auto'),
	path('Articles/<int:id>/<slug:slug>', views.product_details, name = 'product_details'),
	path('faq', views.faq, name = 'faq'),
]

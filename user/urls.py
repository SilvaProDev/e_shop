from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
	path('moncompte', views.index, name = 'moncompte'),
	path('login/', views.login_in, name = 'login'),
	path('logout/', views.logout_func, name = 'logout'),
	path('signup/', views.signup_form, name = 'signup'),
	path('Update-profile/', views.update_profile, name = 'Update-profile'),
	path('user/password', views.user_password, name = 'user_password'),
	#Panel url
	path('user/produits', views.user_orders, name = 'produits'),
	path('user/order-details/<int:id>', views.user_orderdetail, name = 'user_orderdetail'),
	path('orderproduct', views.user_orderproduct, name = 'orderproduct'),
	path('order-product-details/<int:id>/<int:oid>', views.user_order_product_detail, name = 'user_order_product_detail'),

	path('user/comments', views.user_comments, name = 'comments'),
	path('user/delete-comment/<int:id>', views.user_comments_delete, name = 'user_comments_delete'),
	
	
]

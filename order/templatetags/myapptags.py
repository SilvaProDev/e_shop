from django import template
from django.db.models import Count, Avg
from django.db.models import Sum

from django.urls import reverse

from order.models import ShopCart
from product.models import Category
from e_shop import settings


register = template.Library()

@register.simple_tag
def shopcartcount(userid):
    cnt = ShopCart.objects.filter(user_id=userid).count()
    return cnt


from django.db import models
from django.contrib.auth.models import User
from product.models import Produit

# Create your models here.

class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    produit = models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.produit.titre

    @property
    def price(self):
        return self.produit.price

    @property
    def amount(self):
        return (self.produit.price * self.quantity)


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preaparing', 'Preaparing'),
        ('OnShopping', 'OnShopping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=5, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(blank=True, max_length=50)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=150)
    country = models.CharField(blank=True, max_length=150)
    total = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.CharField(blank=True, max_length=150)

    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'commande'
        verbose_name_plural = 'Commandes'

    def __str__(self):
        return self.user.first_name

class OrderProduit(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    amount = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    
    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'commande produit'
        verbose_name_plural = 'Commandes Produits'

    def __str__(self):
        return self.produit.titre


    

    
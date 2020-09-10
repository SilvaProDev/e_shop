from django.shortcuts import render
from django.contrib import messages
from  django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import ShopCart, Order, OrderProduit
from .forms import ShopCartForm, OrderForm
from product.models import Category, Produit, Variant
from user.models import UserProfile

from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def index(request):

    return HttpResponse('hello order')


@login_required(login_url='/login') #verifie si le client est connecté 
def add_to_shop_cart(request, id): #Ajout du produit dans le panier

    url = request.META.get('HTTP_REFERER')
    current_user = request.user #Accède auxs essions de user

    checkoutproduit = ShopCart.objects.filter(produit_id=id) #Verifie si ShopCart(panier) contient des produits
    if checkoutproduit: #Condition de verification si le panier est vide
        control = 1 # Le paner contient des produits
    else:
        control = 0 #il ny a pas de produit dans le panier

    if request.method=='POST':
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control ==1: #On modifie notre ShopCart (si vraiment y a un produit)
                data = ShopCart.objects.get(produit_id=id) #on initialise "data"
                data.quantity += form.cleaned_data['quantity'] #On ajout le produit 
                data.save() #enregistrer le produit dans shopcart
            else: #le produit n'exist pas dans le panier, donc on ajoute le produit
                data = ShopCart() #On inilialise le ShopCart
                data.user_id = current_user.id
                data.produit_id =id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, 'Votre produit a été ajouté avec succès !!')
        return HttpResponseRedirect(url)

    else: # s il n y a pas de post
        if control == 1:
            data = ShopCart.objects.get(produit_id=id)
            data.quantity += 1
            data.save()
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.produit_id=id
            data.quantity = 1
            data.save()
        messages.success(request, 'Votre article  a été ajouté avec success !!')
        return HttpResponseRedirect(url)


@login_required(login_url='/login') #verifie si le client est connecté 
def delete_to_shop_cart(request, id): #Ajout du produit dans le panier

    ShopCart.objects.filter(id=id).delete()
    messages.success(request, 'Votre article a été supprimé .')
    return HttpResponseRedirect('/shop-cart')

def orderproduit(request):
    categorie = Category.objects.all()
    current_user = request.user
    schopcart = ShopCart.objects.filter(user_id=current_user.id)

    total = 0
    for sp in schopcart:
        if sp.produit.variant == 'None':
            total += sp.produit.price * sp.quantity
        else:
            total += sp.variant.price * sp.quantity

    if request.method=='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.country = form.cleaned_data['country']
            data.user_id =current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()
            data.code = ordercode
            data.save() 

            subject = "Validation de votre Achat sur Tshop"
            from_email = settings.EMAIL_HOST_USER
            to_email = [current_user.email]
            body = "Félicitation vous venez de valider votre achat sur https://e-trashop.herokuapp.com \n Voici la reference de votre produit {} Nous vous enverons un email".format(ordercode)
            send_mail(subject=subject, from_email=from_email, recipient_list=to_email, message=body, fail_silently=False)


            #Move the ShopCart items to Orders Product items
            schopcart = ShopCart.objects.filter(user_id=current_user.id)
            for sp in schopcart:
                details = OrderProduit()
                details.order_id= data.id #Order id
                details.produit_id = sp.produit_id
                details.user_id = current_user.id
                details.quantity = sp.quantity
                if sp.produit.variant == 'None':
                    details.price = sp.produit.price
                else:
                    details.price = sp.variant.price

                details.variant_id = sp.variant_id
                details.amount = sp.amount
                details.save()

                #Reduce quantity of sold produit  from amount of produit
                if sp.produit.variant == 'None':
                    produit = Produit.objects.get(id=sp.produit_id)
                    produit.amount -= sp.quantity
                    produit.save()
                else:
                    variant = Variant.objects.get(id=sp.produit_id)
                    variant.amount -= sp.quantity
                    variant.save()
            
            ShopCart.objects.filter(user_id = current_user.id).delete() #Supprime les produit dans shopcart
            request.session['cart_items']=0
            messages.success(request, 'Your has been completed, thank you')
            return render(request, 'pages/order-completed.html', {'ordercode':ordercode, 'categorie':categorie})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/order/orderproduit')

    form = OrderForm()
    profile = UserProfile.objects.get(user_id= current_user.id)
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    context = {'schopcart':schopcart,
        'categorie':categorie,
        'total':total,
        'form':form,
        'profile':profile,
        }
    return render(request, 'pages/order-form.html', context)
	
	

	
	
		
	

	

    
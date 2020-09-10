from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Setting, ContactMessage, Faq
from .forms import ContactForm, SearchForm
from product.models import Category, Produit, Image, Comment, Variant, Color, Size
from order.models import ShopCart

from django.conf import settings
from django.core.mail import send_mass_mail

from newsletters.models import NewsletterUser,Newsletters
from newsletters.forms import NewsletterUserSignUp

# Create your views here.
def index(request):
	if request.method =='POST':
		form1 = NewsletterUserSignUp(request.POST)
		if form1.is_valid():
			instance = NewsletterUser()
			instance.email = form1.cleaned_data['email']
			instance.save()
			
	form1 = NewsletterUserSignUp
	page = 'home'
	setting = Setting.objects.get(pk=1)
	#categorie = Category.objects.all()
	product_slider = Produit.objects.all().order_by('-id')[:6] #Les 5 novo articles ajouté
	product_latest = Produit.objects.all().order_by('id')[:8] #Les 5 novo articles ajouté
	product_picker = Produit.objects.all().order_by('?')[:8] #Les 5 novo articles ajouté
	product = Produit.objects.all().order_by('-date_add')[:8] #Les 5 novo articles ajouté

	context = {
		"form1":form1,
		'setting':setting,
		'page':page,
		#'categorie':categorie,
		'product_slider':product_slider,
		'product_latest':product_latest,
		'product_picker':product_picker,
		'product':product,
	}
	return render(request, 'pages/index.html', context)

def aboutus(request):
	categorie = Category.objects.all()
	setting = Setting.objects.get(pk=1)

	context = {
		'setting':setting,'categorie':categorie,
	}
	return render(request, 'pages/aboutus.html', context)

def contactus(request):

	if request.method=='POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			data = ContactMessage()
			data.name = form.cleaned_data['name']
			data.email = form.cleaned_data['email']
			data.subject = form.cleaned_data['subject']
			data.message = form.cleaned_data['message']
			data.ip = request.META.get('REMOTE_ADDR')
			data.save()
			messages.success(request, 'Votre message a bien été envoyé merci de nous avoir contacter !!')
			return HttpResponseRedirect('/contact-us')

	categorie = Category.objects.all()
	setting = Setting.objects.get(pk=1)
	form = ContactForm
	context = {'categorie':categorie,'setting':setting,'form':form}

	return render(request, 'pages/contactus.html', context)

	
def product_categorie(request, id, slug):

	categorie = Category.objects.all()
	produits = Produit.objects.filter(categorie_id=id)
	catdata = Category.objects.get(pk=id)
	context = {'produits':produits,'categorie':categorie, 'catdata':catdata}

	return render(request, 'pages/product_categorie.html', context)

def search(request):
	if request.method=='POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			query = form.cleaned_data['query']
			catid = form.cleaned_data['catid']

			if catid==0:
				produits = Produit.objects.filter(titre__icontains=query)
			else:
				produits = Produit.objects.filter(titre__icontains=query, categorie_id=catid)


			categorie = Category.objects.all()
			context = {'produits':produits,'categorie':categorie, 'query':query}

			return render(request, 'pages/search.html', context)

	return HttpResponseRedirect('/')


def search_auto(request):
	if request.is_ajax():
		q = request.GET.get('term', '')
		produits = Produit.objects.filter(titre__icontains=q)
		results = []
		for rs in produits:
			place_json = {}
			place_json = rs.titre
			results.append(place_json)
		data = json.dumps(results)
	else:
		data = 'fail' 	
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)


def product_details(request, id, slug):
	query = request.GET.get('q')
	categorie = Category.objects.all()
	produit = Produit.objects.get(pk=id)
	img = Image.objects.filter(product_id=id)
	comment = Comment.objects.filter(produit_id=id, status='Red')

	#Affichage des avis des clients 
	
	#review = Comment.objects.filter(produit_id=id, status='Red').aggregate(Count('id'),Avg('rate'))
	#Retrieve_values: review.rate__avg, review.id__count
	#review = Comment.objects.row("SELECT,id, count(id) as countrew, avg(rate) as avgrew for product_comment WHERE produit_id=%s and status = 'Red'", [id])[0]
	#Retrieve_values: review.avgrew, review.countrew
	context = {'produit':produit, 'categorie':categorie, 
			   'img':img, 'comment':comment,
		}
	if produit.variant != "None":
		if request.method == "POST":
			variant_id= request.POST.get('variantid')
			variant = Variant.objects.get(id=variant_id)
			colors = Variant.objects.filter(produit_id=id, size_id=variant.size_id)
			sizes = Variant.objects.raw('SELECT * FROM  product_variant WHERE produit_id=%s GROUP BY size_id,product_variant.id', [id])
			query += variant.titre+'Size:'+str(variant.size)+'Color:'+str(variant.color)
		else:
			variants = Variant.objects.filter(produit_id=id)
			colors = Variant.objects.filter(produit_id=id, size_id=variants[0].size_id)
			sizes = Variant.objects.raw('SELECT * FROM product_variant WHERE produit_id =%s GROUP BY size_id, product_variant.id', [id])
			variant = Variant.objects.get(id=variants[0].id)
		context.update({'sizes':sizes,'color':colors,'variant':variant,'query':query,})

	return render(request, 'pages/product_details.html', context)

# def ajaxcolor(request):
# 	data = {}
# 	if request.POST.get('action') == 'post':
# 		size_id= request.POST.get('size')
# 		produitid = request.POST.get('produitid')
# 		colors = Variant.objects.filter(produit_id=produitid, size_id=size_id)
# 		context = {
# 			'size_id':size_id,
# 			'produitid':produitid,
# 			'colors':colors,
# 		}
# 		data = {'rendered_table':render_to_string('pages/color_list.html', context=context)}
# 		return JsonResponse(data)
# 	return JsonResponse(data)
@csrf_exempt
def ajaxcolors(request):
	data = {}
	if request.POST.get('action') == "post":
		size_id = request.POST.get('size')
		produitid = request.POST.get('produitid')
		colors = Variant.objects.filter(produit_id=produitid, size_id=size_id)
		context = {
			'size_id':size_id,
			'produitid':produitid,
			'colors':colors,
		}
		data = {'rendered_table': render_to_string('pages/color_list.html',context)}
		return JsonResponse(data)
	return JsonResponse(data)

@login_required(login_url='/login')
def shop_cart(request):
	categorie = Category.objects.all()
	current_user = request.user
	shopcart = ShopCart.objects.filter(user_id= current_user.id)

	total = 0
	for sp in shopcart:
		total += sp.produit.price * sp.quantity
	context = {'shopcart':shopcart,'categorie':categorie,'total':total}

	return render(request, 'pages/shop-cart-product.html', context)

def faq(request):

	setting = Setting.objects.get(pk=1)
	categorie = Category.objects.all()
	faq = Faq.objects.filter(status="True").order_by("ordernumber")

	context = {'faq':faq,'categorie':categorie,'setting':setting}

	return render(request, 'pages/faq.html', context)




    	
    	
    	
    	
    	
    	
			
    	
  	
  

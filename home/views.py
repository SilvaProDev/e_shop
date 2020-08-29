from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Setting, ContactMessage, Faq
from .forms import ContactForm, SearchForm
from product.models import Category, Produit, Image, Comment
from order.models import ShopCart

from django.conf import settings
from django.core.mail import send_mail

from newsletter.models import NewsletterUser,Newsletter
from newsletter.forms import NewsletterSignUpForm

# Create your views here.
def index(request):
	if request.method =='POST':
		form = NewsletterSignUpForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			data = NewsletterUser.objects.create(email=email)
			# instance = form.save()
			newsletter = Newsletter.objects.get(id=data.id)
			if newsletter.status==True:
				subject = newsletter.subject
				body = newsletter.body
				from_email = settings.EMAIL_HOST_USER
				for email in newsletter.email.all():
					send_mail(subject=subject, from_email=from_email, recipient_list=[email], message=body, fail_silently=True)

	form = NewsletterSignUpForm()
	page = 'home'
	setting = Setting.objects.get(pk=1)
	categorie = Category.objects.all()
	product_slider = Produit.objects.all().order_by('-id')[:6] #Les 5 novo articles ajouté
	product_latest = Produit.objects.all().order_by('id')[:8] #Les 5 novo articles ajouté
	product_picker = Produit.objects.all().order_by('?')[:12] #Les 5 novo articles ajouté

	context = {
		"form":form,
		'setting':setting,
		'page':page,
		'categorie':categorie,
		'product_slider':product_slider,
		'product_latest':product_latest,
		'product_picker':product_picker,
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
	categorie = Category.objects.all()
	produit = Produit.objects.get(pk=id)
	img = Image.objects.filter(product_id=id)
	comment = Comment.objects.filter(produit_id=id, status='Red')

	#Affichage des avis des clients 
	
	#review = Comment.objects.filter(produit_id=id, status='Red').aggregate(Count('id'),Avg('rate'))
	#Retrieve_values: review.rate__avg, review.id__count
	#review = Comment.objects.row("SELECT,id, count(id) as countrew, avg(rate) as avgrew for product_comment WHERE produit_id=%s and status = 'Red'", [id])[0]
	#Retrieve_values: review.avgrew, review.countrew

	context = {'produit':produit,'categorie':categorie, 'img':img,'comment':comment,}

	return render(request, 'pages/product_details.html', context)


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




    	
    	
    	
    	
    	
    	
			
    	
  	
  

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect



from product.models import Category, Comment
from user.models import UserProfile
from order.models import Order, OrderProduit
from . forms import signUpForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.
@login_required(login_url='/login') 
def index(request):
    #categorie = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id= current_user.id)
    
    
    context = {
        #'categorie':categorie,
        'profile':profile,
        }
    return render(request, 'user/user-profile.html', context)

def login_in(request):

    if request.method=='POST': #s'il y eu envoie de formulaire
        #On verifie le username et le password
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
            #I l'utilisateur est connecté on renvoie la page d'accueil
            messages.success(request, 'vous êtes bien connecté  '+ user.username )
            return HttpResponseRedirect('/')      
            
        else:
            messages.success(request, 'Login Error ! Nomutilisateur ou mot de passe incorrect')
            return HttpResponseRedirect('/login') #Renvoie tjrs la page de connexion
            
    #categorie = Category.objects.all()
    context = {
        #'categorie':categorie,
        }
    return render(request, 'user/login_form.html', context)

def logout_func(request):
    
    logout(request)
    return HttpResponseRedirect('/')

def signup_form(request):
    if request.method=='POST':
        form = signUpForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data['username']
            # email = form.cleaned_data['email']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # password = form.cleaned_data['password']
            # User.objects.create_user(username=username, email=email,  first_name=first_name,
            #  last_name=last_name, password=password)

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            #Créer un profile par defaut
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = 'images/users/user.jpg'
            data.save()

            messages.success(request, 'Votre compte a été crée avec succèss !!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/signup')
    
    else:
        form = signUpForm()
    #categorie = Category.objects.all()
    context = {
        #'categorie':categorie,
        'form':form,}
    return render(request, 'user/signup_form.html', context)
    

@login_required(login_url='/login')
def update_profile(request):
    if request.method=='POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Votre Profile a été modifier avec success !')
            return redirect('/moncompte')

    else:
        #categorie = Category.objects.all()
        user_form = UserUpdateForm( instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            #'categorie':categorie,
            'user_form':user_form,
            'profile_form':profile_form,
            }
        return render(request, 'user/update_profile.html', context)

@login_required(login_url='/login') 
def user_password(request):
    if request.method=='POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request, 'Votre mode passe a été changé avec success')
            return HttpResponseRedirect('/Mon-Compte')
        else:
            messages.error(request, 'Vous avez saisi un mot de passe incorrect. <br>'+str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        #categorie = Category.objects.all()
        form = PasswordChangeForm(request.user)
        context = {
            #'categorie':categorie,
            'form':form,
            
            }
        return render(request, 'user/user_password.html', context)

@login_required(login_url='/login') 
def user_orders(request):

    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)

    #categorie = Category.objects.all()
    
    context = {
        #'categorie':categorie,
        'orders':orders,
        
        }
    return render(request, 'user/my-products.html', context)


@login_required(login_url='/login') 
def user_orderdetail(request, id):

    current_user = request.user
    orders = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduit.objects.filter(order_id=id)

    #categorie = Category.objects.all()
    
    context = {
        #'categorie':categorie,
        'orders':orders,
        'orderitems':orderitems,
        
        }
    return render(request, 'user/user-order-details.html', context)


@login_required(login_url='/login') 
def user_orderproduct(request):

    current_user = request.user
    order_product = OrderProduit.objects.filter(user_id=current_user.id)

    #categorie = Category.objects.all()
    
    context = {
        #'categorie':categorie,
        
        'order_product':order_product,
        
        }
    return render(request, 'user/user_order_products.html', context)

    
@login_required(login_url='/login') 
def user_order_product_detail(request, id, oid):
    current_user = request.user
    orders = Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderProduit.objects.filter(id=id, user_id=current_user.id)

    #categorie = Category.objects.all()
    
    context = {
        #'categorie':categorie,
        'orders':orders,
        'orderitems':orderitems,
        
        }
    return render(request, 'user/user-order-product-detail.html', context)


def user_comments(request):

    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    #categorie = Category.objects.all()
    
    context = {
        #'categorie':categorie,
        'comments':comments,
        
        }
    return render(request, 'user/user-comments.html', context)


@login_required(login_url='/login') 
def user_comments_delete(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Votre message est supprmé avec success !! .')
    return HttpResponseRedirect('/user/comments')





    



    

    

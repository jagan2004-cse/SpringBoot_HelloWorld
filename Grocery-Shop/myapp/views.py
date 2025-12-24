from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model,authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product,Cart,CartItem
from .forms import LoginForm,SignupForm
from django.db.models import Q

User = get_user_model()

def home(request):
    return render(request,'home.html')

@login_required(login_url='/login')
def products(request):
    products = Product.objects.all()
    return render(request,'products.html',{ 'products': products })

@login_required(login_url='/login')
def product(request,id):
    product = Product.objects.filter(id = id).first()
    if product:
        related = Product.objects.filter(Q(category = product.category) | Q(brand = product.brand)).exclude(id = product.id)
    else:
        related = []
    return render(request,'product.html',{ 'product': product, 'related_products': related })

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            # email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'home')  
                return redirect(next_url)
            else:
                messages.info(request, 'Invalid Credentials!')
                return redirect('login')
    else:
        form = LoginForm()
    return render(request,'login.html',{'form' : form})

def user_signup(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password']
            password2 = form.cleaned_data['confirmPassword']
            if(password1 != password2):
                messages.info(request, 'Passwords do not match!')
            elif User.objects.filter(email = email).exists():
                messages.info(request,'Email already Taken!')
            elif User.objects.filter(username = username).exists():
                messages.info(request,'Username already Taken!')
            else:
                user = User.objects.create_user(username=username,email=email,password=password1)
                user.save()
                return redirect('login')
            return render(request,'signup.html',{'form' : form})  
    else:
        form = SignupForm()
    return render(request,'signup.html',{'form' : form})    

@login_required(login_url='/login')
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/login')
def cart(request):
    cart,created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    return render(request,'cart.html',{'cart':cart,'cart_items':cart_items})

@login_required(login_url='/login')
def add_to_cart(request,id):
    product = Product.objects.get(id=id)
    cart,created = Cart.objects.get_or_create(user = request.user)
    cart_item,created = CartItem.objects.get_or_create(cart = cart,product = product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return JsonResponse({
        'success': True,
        'message': f"{product.name} added to Cart Successfully"
    })

@login_required(login_url='/login')
def add_item(request,id):
    product = Product.objects.get(id=id)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart,product=product)
    cart_item.add_item()
    return JsonResponse({
        'success': True,
        'quantity': cart_item.quantity,
        'total_price': cart.cart_price
    })

@login_required(login_url='/login')
def remove_item(request,id):
    product = Product.objects.get(id=id)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart,product=product)
    cart_item.remove_item()
    return JsonResponse({
        'success': True,
        'quantity': cart_item.quantity,
        'total_price': cart.cart_price
    })



from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from products.models import Product
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.

@csrf_exempt
def register(request):
    if request.method == "POST":
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        username = request.POST["username"]
        password1 = request.POST["psw"]
        password2 = request.POST["psw-repeat"]

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                return redirect("register")
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password1,
                    email=email,
                    first_name=firstname,
                    last_name=lastname,
                )
                messages.success(request, 'User registered successfully.')
                return redirect("login")
        else:
            messages.error(request, 'User registration Failed. Please try again!!')
            return redirect("register")

    else:
        return render(request, "register.html")


def home(request):
    return render(request, "home.html")


def addproduct(request):
    return render(request, "addproduct.html")


@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'User logged in successfully.')
            return redirect("products")
        else:
            messages.error(request, 'Authentication Unsuccessful. Please try again with correct credentials.!!')
            return redirect("login")

    else:
        return render(request, "login.html")


def add_pagination(request, all_data):
    page = request.GET.get('page', 1)
    paginator = Paginator(all_data, 10)
    try:
        all_data = paginator.page(page)
    except PageNotAnInteger:
        all_data = paginator.page(1)
    except EmptyPage:
        all_data = paginator.page(paginator.num_pages)
    return all_data


def products(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")

        Product.objects.create(name=name, price=price, username=request.user.get_full_name())
        messages.success(request, 'Product added successfully.')
        return redirect("products")
    else:
        f = []
        qs = Product.objects.get_queryset().order_by('-id').filter(username=request.user.get_full_name())
        for e in qs:
            data = Product()
            data.id = e.id
            data.name = e.name
            data.price = e.price
            data.username = e.username
            f.append(data)

        final_data = add_pagination(request, f)

    return render(request, "products.html", {"data": final_data})


def delproduct(request, id):
    Product.objects.filter(id=id).delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect("products")


@csrf_exempt
def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout Successful.')
    return redirect("/")

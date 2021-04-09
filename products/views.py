from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from products.models import Product


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
                return redirect("login")
        else:
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
            try:
                user_data = User.objects.get(username=username)
            except:
                user_data = None
            return redirect("products", user_data)
        else:
            return redirect("login")

    else:
        return render(request, "login.html")


def products(request, user_data):
    if request.method == "POST":

        name = request.POST.get("name")
        price = request.POST.get("price")
        username = user_data

        Product.objects.create(name=name, price=price, username=user_data)
        return redirect("products")
    else:
        f = []
        qs = Product.objects.all()

        for e in qs:
            data = Product()
            data.id = e.id
            data.name = e.name
            data.price = e.price
            data.username = e.username
            f.append(data)

    return render(request, "products.html", {"data": f})


@csrf_exempt
def logout(request):
    auth.logout(request)
    return redirect("/")

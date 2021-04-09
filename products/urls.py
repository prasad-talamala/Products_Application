from django.conf.urls import url
from django.urls import path

from products import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("addproduct", views.addproduct, name="addproduct"),
    url(r'^products/(?:(?P<user_data>\w{1,}))?$', views.products, name="products"),
]

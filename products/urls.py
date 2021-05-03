from django.conf.urls import url
from django.urls import path, re_path

from products import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("addproduct", views.addproduct, name="addproduct"),
    path("products", views.products, name="products"),
    re_path(r'^delproduct/(?P<id>\d+)$', views.delproduct, name='delproduct'),
]

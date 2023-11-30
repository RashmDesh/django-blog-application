from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('register/', views.register),
    path("update/", views.update),
    path("registerotp/", views.registerotp),
    path("updateotp/", views.updateotp),
    path("logout/", views.logout),
    path("loginresult/", views.loginresult),


]

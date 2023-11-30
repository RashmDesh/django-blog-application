from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog),
    path("addblog/", views.BlogAdd.as_view()),
    path("blogapi/", views.BlogApi.as_view()),
]

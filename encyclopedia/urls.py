from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("random_page", views.random_page, name="random_page"),
    path("<str:title>", views.article, name="article")
]

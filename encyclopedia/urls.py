from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("random_page", views.random_page, name="random_page"),
    path("article/<str:title>", views.article, name="article"), 
    path("new_page", views.new_page, name="new_page"),
    path("error", views.error, name="error"),
    path("edit_page/<str:title>", views.edit_page, name="edit_page")
]

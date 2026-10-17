from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("book/<int:pk>/", views.book_detail, name="book_detail"),
    path("subscribe/", views.subscribe, name="subscribe"),
]

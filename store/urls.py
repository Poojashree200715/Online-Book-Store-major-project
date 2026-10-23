from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("book/<int:pk>/", views.book_detail, name="book_detail"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("checkout/", views.checkout, name="checkout"),
    path("order/<int:pk>/", views.order_confirmation, name="order_confirmation"),
]

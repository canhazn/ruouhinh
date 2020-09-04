from django.urls import path
from product import views


urlpatterns = [
    path('cua-hang/<slug:slug>/',
         views.ProductDetailView.as_view(), name="product-detail"),
    path('thanh-toan/', views.checkout, name="checkout"),
    path('thanh-toan-thanh-cong/<int:pk>/', views.confirmation,
         name="thanh-toan-thanh-cong")
]

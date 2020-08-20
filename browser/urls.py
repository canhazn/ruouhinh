from django.urls import path
from browser import views

urlpatterns = [
    path('', views.homePage, name="trang-chu"),
]

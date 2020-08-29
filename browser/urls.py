from django.urls import path
from browser import views

urlpatterns = [
    path('', views.homePage, name="trang-chu"),
    path('qui-trinh-nau-ruou-trang/', views.quitrinh,
         name="qui-trinh-nau-ruou-trang"),
    path('li-do-mua-ruou-trang-tu-ruou-hinh/',
         views.lido, name="li-do-mua-ruou-trang")
]

from django.shortcuts import render
from product import models


def homePage(request):
    queryset = models.Product.objects.all()

    return render(request, 'index.html', {
        "app_url": "home",
        "products": queryset
    })


def lido(request):
    return render(request,  "li_do_mua_ruou_trang.html", {
        "app_url": "li-do",
    })


def quitrinh(request):
    return render(request,  "qui_trinh_nau_ruou_trang.html", {
        "app_url": "qui-trinh",
    })


def shop(request):
    queryset = models.Product.objects.all()

    return render(request,  "shop.html", {
        "app_url": "cua-hang",
        "products": queryset
    })


def contact(request):

    return render(request,  "contact.html", {
        "app_url": "lien-he",
    })

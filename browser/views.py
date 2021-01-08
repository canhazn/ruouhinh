from django.shortcuts import render, redirect
from django.core.mail import send_mail


def homePage(request):
    context = {
        "form": ""
    }

    return render(request, 'index.html', context)


def lido(request):
    return render(request,  "li_do_mua_ruou_trang.html", {
        "app_url": "li-do",
    })


def quitrinh(request):
    return render(request,  "qui_trinh_nau_ruou_trang.html", {
        "app_url": "qui-trinh",
    })


def contact(request):
    return render(request,  "contact.html", {
        "app_url": "lien-he",
    })

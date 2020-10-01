from django.shortcuts import render, redirect
from product import models, forms
from django.core.mail import send_mail


def homePage(request):

    if request.method == "POST":
        form = forms.OrderForm(request.POST)
        if form.is_valid():
            instance = form.save()
            message = "%s - %s - %s - %s - %s" % (instance.phone,
                                                  instance.name,
                                                  instance.address,
                                                  instance.quantity,
                                                  instance.note)
            send_mail(subject="Money coming babe :)", message=message,
                      from_email='ruouhinh@gmail.com',
                      recipient_list=["canhazn@gmail.com"],
                      fail_silently=False)
            # print(instance)
            return redirect("thanh-toan-thanh-cong", instance.id)

    else:
        print("fomr invalid")

    context = {
        "form": forms.OrderForm()
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

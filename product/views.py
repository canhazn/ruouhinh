from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from product import models, forms
from django.core.mail import send_mail


class ProductDetailView(generic.DetailView):
    model = models.Product
    queryset = models.Product.objects.all()
    template_name = "product_details.html"


def checkout(request):
    slug = request.GET.get('product')
    quantity = request.GET.get('quantity')

    product = get_object_or_404(models.Product, slug=slug)

    if request.method == "POST":
        form = forms.OrderForm(request.POST)
        if form.is_valid():
            instance = form.save()
            message = "%s - %s - %s - %s - %s" % (instance.customer,
                                                  instance.address,
                                                  instance.phone,
                                                  instance.quantity,
                                                  product.name)
            send_mail(subject="Money coming babe :)", message=message,
                      from_email='ruouhinh@gmail.com',
                      recipient_list=["canhazn@gmail.com"],
                      fail_silently=False)
            # print(instance)
            return redirect("thanh-toan-thanh-cong", instance.id)

    else:
        print("fomr invalid")

    context = {
        "product": product,
        "quantity": quantity,
        "form": forms.OrderForm()
    }
    return render(request, "checkout.html", context)


def confirmation(request, pk):

    order = get_object_or_404(models.Order, id=pk)
    product = get_object_or_404(models.Product, id=order.product.id)
    print(product)

    context = {
        "order": order,
        "product": product
    }

    return render(request, "confirmation.html", context)

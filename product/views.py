from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from product import models, forms


class ProductDetailView(generic.DetailView):
    model = models.Product
    queryset = models.Product.objects.all()
    template_name = "product_details.html"


def checkout(request):
    slug = request.GET.get('product')
    quantity = request.GET.get('quantity')

    product = get_object_or_404(models.Product, slug=slug)

    if request.method == "POST":
        print(request.body)
        form = forms.OrderForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect("thanh-toan-thanh-cong")

    context = {
        "product": product,
        "quantity": quantity,
        "form": forms.OrderForm()
    }
    return render(request, "checkout.html", context)


def confirmation(request):
    return render(request, "confirmation.html")

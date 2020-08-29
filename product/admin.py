from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from product import models


class ProductAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(models.Product, ProductAdmin)


class OrderAdmin(SummernoteModelAdmin):
    list_display = ["customer", "product",
                    "quantity", "address", "note", "delivered"]


admin.site.register(models.Order, OrderAdmin)

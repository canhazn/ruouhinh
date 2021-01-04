from django.contrib import admin
from core import models


class ProductAdmin(admin.ModelAdmin):
    list_display = ["title"]
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(models.Product, ProductAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ["customer_name"]


admin.site.register(models.Order, OrderAdmin)


class MaterialAdmin(admin.ModelAdmin):
    list_display = ["title"]


admin.site.register(models.Material, MaterialAdmin)


class ReceiptAdmin(admin.ModelAdmin):
    list_display = ["factory", "material"]


admin.site.register(models.Receipt, ReceiptAdmin)

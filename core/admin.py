from django.contrib import admin
from core import models
from django.db.models import Sum

class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "price"]

admin.site.register(models.Product, ProductAdmin)


class CargoAdmin(admin.ModelAdmin):
    list_display = ["id", "employer", "product", "quantity", "real_quantity", "date_created"]
    
    def real_quantity(self, obj):        
        orders = models.Order.objects.filter(cargo=obj.id)
        quantity_sum = orders.aggregate(Sum('quantity')).get("quantity__sum")
        if quantity_sum is None:
            return obj.quantity
        else:
            return obj.quantity - quantity_sum


admin.site.register(models.Cargo, CargoAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "customer_name" , "employer","total_cost"]
    # list_display = ["id", "customer_name" , "employer", "product","total_cost"]


admin.site.register(models.Order, OrderAdmin)


class MaterialAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]


admin.site.register(models.Material, MaterialAdmin)


class ReceiptAdmin(admin.ModelAdmin):
    list_display = ["material"]


admin.site.register(models.Receipt, ReceiptAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ["email"]


admin.site.register(models.User, UserAdmin)


class NotificationAdmin(admin.ModelAdmin):
    raw_id_fields = ('recipient',)
    list_display = ('recipient', 'actor',
                    'target', 'verb')
    list_filter = ('level', 'unread', 'public', 'timestamp',)

    def get_queryset(self, request):
        qs = super(NotificationAdmin, self).get_queryset(request)
        return qs.prefetch_related('actor')


admin.site.register(models.Notification, NotificationAdmin)

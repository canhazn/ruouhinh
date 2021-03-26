from django.contrib import admin
from core import models


class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "price"]


admin.site.register(models.Product, ProductAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "customer_name" , "employer", "total_cost"]


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

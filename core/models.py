from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin
from notifications.base.models import AbstractNotification


class User(AbstractUser):
    # Delete not use field
    username = None
    last_login = None
    # is_staff = None
    # is_superuser = None

    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    factory_name = models.CharField(max_length=255)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Notification(AbstractNotification):
    # custom field example
    # category = models.ForeignKey('myapp.Category',
    #                              on_delete=models.CASCADE)

    class Meta(AbstractNotification.Meta):
        abstract = False
        app_label = 'core' 



class Product(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)    
    price = models.IntegerField(default=0)
    # description = models.TextField(null=False, blank=False)

    def __str__(self):
        return str(self.title)


class Inventory(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=1)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return "%s" % (self.title)


class Order(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE,  default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False)
    customer_name = models.CharField(max_length=200, null=False, blank=False)
    note = models.CharField(max_length=200, null=True, blank=True, default="")
    date_created = models.DateTimeField(auto_now_add=True)
    total_cost = models.FloatField(null=False, blank=False, default=0)
    completed = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return "Order: %s - %s" % (str(self.customer_name), str(self.employer.factory_name))


class Material(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return str(self.title)


class Receipt(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=200, null=True, blank=True, default="")
    completed = models.BooleanField(default=True)
    quantity = models.IntegerField(null=False, blank=False)
    total_cost = models.FloatField(null=False, blank=False, default=0)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return "Receipt: %s - %s" %(str(self.material.title), str(self.employer.factory_name))

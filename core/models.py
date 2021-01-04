from django.db import models
from django.contrib.auth.models import User


class Factory(models.Model):
    title = models.CharField(max_length=200, null=False,
                             blank=False, default="Rượu Hinh")
    address = models.TextField(null=False, blank=False)
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return "%s" % (str(self.address))


class Product(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(max_length=200, null=False, blank=False)
    price = models.IntegerField(default=0)
    description = models.TextField(null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return str(self.title)


class Issue(models.Model):
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return "%s" % (self.title)


class ProductIssue(models.Model):
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=1)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return "Factory: %s, Product: %s, Quantity: %s" % (self.factory, self.product, str(self.quantity))


class Order(models.Model):
    customer_name = models.CharField(max_length=200, null=False, blank=False)
    phone = models.CharField(max_length=20, null=False, blank=False)
    address = models.CharField(max_length=200, null=False, blank=False)
    note = models.CharField(max_length=200, null=True, blank=True, default="")
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return str(self.customer_name)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def _get_total_cost(self):
        "Returns the total cost of item"
        return self.product.price * self.quantity
    total_cost = property(_get_total_cost)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return "%s, %s" % (str(self.name), str(self.quantity))


class Material(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return str(self.title)


class Receipt(models.Model):
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(null=False, blank=False)
    total_cost = models.FloatField(null=False, blank=False, default=0)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return "%s" % (self.factory)

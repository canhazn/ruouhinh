from django.db import models


def path_file_name(instance, filename):
    newName = "_".join(filter(None, (instance.slug, filename)))
    return "%s/%s/%s" % ('ruou-hinh', instance.slug, newName)


class Product(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(max_length=200, null=False, blank=False)
    price = models.IntegerField(default=0)
    content = models.TextField(null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    thumb = models.ImageField(upload_to=path_file_name, null=True)
    available = models.BooleanField(default=True)
    available_on = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return str(self.name)


class Order(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    phone = models.CharField(max_length=20, null=False, blank=False)
    address = models.CharField(max_length=200, null=False, blank=False)
    note = models.CharField(max_length=200, null=True, blank=True, default="")
    created_on = created_on = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(null=False, blank=False)
    delivered = models.BooleanField(default=False)

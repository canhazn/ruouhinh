from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.save()
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suppors using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    factory_name = models.CharField(max_length=255)    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


# class Profile(models.Model):
#     """
#     User profile == Factory profile
#     """
#     address = models.TextField(null=False, blank=False)
#     user = models.OneToOneField(
#         User, on_delete=models.DO_NOTHING, null=True, blank=True)
#     date_created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ["-date_created"]

#     def __str__(self):
#         return "%s" % (str(self.address))


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
    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return "%s" % (self.title)


class ProductIssue(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=1)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return "Profile: %s, Product: %s, Quantity: %s" % (self.employer, self.product, str(self.quantity))


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
    employer = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(null=False, blank=False)
    total_cost = models.FloatField(null=False, blank=False, default=0)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return "%s" % (self.employer)

from core import models, serializers
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class FactoryViewSet(viewsets.ModelViewSet):
    """
    Factory serializer
    """
    queryset = models.Factory.objects.all()
    serializer_class = serializers.FactorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    """
    Product serializer
    """
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductIssueViewSet(viewsets.ModelViewSet):
    """
    ProductIssue serializer
    """
    queryset = models.ProductIssue.objects.all()
    serializer_class = serializers.ProductIssueSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MaterialViewSet(viewsets.ModelViewSet):
    """
    Material serializer
    """
    queryset = models.Material.objects.all()
    serializer_class = serializers.MaterialSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ReceiptViewSet(viewsets.ModelViewSet):
    """
    Receipt serializer
    """
    queryset = models.Receipt.objects.all()
    serializer_class = serializers.ReceiptSerializer

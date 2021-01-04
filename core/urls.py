from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'factory', views.FactoryViewSet)
router.register(r'product', views.ProductViewSet)
router.register(r'product-issue', views.ProductIssueViewSet)

# Material
router.register(r'material', views.MaterialViewSet)
router.register(r'receipt', views.ReceiptViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

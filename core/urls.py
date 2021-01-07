from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "core_api"

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'product', views.ProductViewSet)
router.register(r'product-issue', views.ProductIssueViewSet)

# Material
router.register(r'material', views.MaterialViewSet)
router.register(r'receipt', views.ReceiptViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('logout/blacklist/', views.BlacklistTokenUpdateView.as_view(),
         name='blacklist')
]

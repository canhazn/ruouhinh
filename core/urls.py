from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core import views
from rest_framework_simplejwt.views import (    
    TokenRefreshView,
)
from rest_framework.urlpatterns import format_suffix_patterns


app_name = "core_api"

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
# router.register(r'product', views.ProductViewSet)
# router.register(r'issue', views.IssueViewSet)
# router.register(r'material', views.MaterialViewSet)

# Material
# router.register(r'receipt', views.ReceiptViewSet)
# router.register(r'order', views.OrderViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('token/', views.UserLoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/blacklist/', views.BlacklistTokenUpdateView.as_view(),
         name='blacklist')
]

urls = format_suffix_patterns([
    path('receipt/', views.ReceiptList.as_view()),
    path('receipt/<int:pk>/', views.ReceiptDetail.as_view()),

    path('order/', views.OrderList.as_view()),
    path('order/<int:pk>/', views.OrderDetail.as_view()),
])

urlpatterns += urls

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core import views
from rest_framework_simplejwt.views import (    
    TokenRefreshView, TokenObtainPairView
)
from rest_framework.urlpatterns import format_suffix_patterns


# The API URLs are now determined automatically by the router.
urlpatterns = [    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/blacklist/', views.BlacklistTokenUpdateView.as_view(),
         name='blacklist')
]

urls = format_suffix_patterns([
    path('receipt/', views.ReceiptList.as_view()),
    path('receipt/<int:pk>/', views.ReceiptDetail.as_view()),

    path('order/', views.OrderList.as_view()),
    path('order/<int:pk>/', views.OrderDetail.as_view()),

    path('product/', views.ProductList.as_view()),
    path('material/', views.MaterialList.as_view()),

    path('cargo/', views.CargoList.as_view()),
    path('cargo/<int:pk>/', views.CargoDetail.as_view()),


    path('notify/', views.get_notify),
    path('get_factory_name/', views.get_factory_name)
])

urlpatterns += urls

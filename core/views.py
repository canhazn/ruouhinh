from core import models, serializers
from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework import permissions

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view


class UserLoginView(APIView):
    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            user = authenticate(
                request,
                email=request.data["email"],
                password=request.data["password"]
            )

            if user:
                refresh = TokenObtainPairSerializer.get_token(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'access_expires': int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
                    'refresh_expires': int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
                    "user": {
                        "email": user.get_username(),
                        "factory_name": user.__getattribute__("factory_name")
                    }
                }
                return Response(data, status=status.HTTP_200_OK)
            return Response({
                'error_message': 'Email or password is incorrect!',
                'error_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'error_messages': serializer.errors,
            'error_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(viewsets.ModelViewSet):
    """
    Product serializer
    """
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class IssueViewSet(viewsets.ModelViewSet):
    """
    Issue serializer
    """
    queryset = models.Issue.objects.all()
    serializer_class = serializers.IssueSerializer
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
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['material']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """ Perform create """
        serializer.save(employer=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    """
    Order serializer
    """
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['customer_name', 'note']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """ Perform create """
        serializer.save(employer=self.request.user)

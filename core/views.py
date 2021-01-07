from core import models, serializers
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.settings import api_settings
from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken


from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


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

    def perform_create(self, serializer):
        """ Perform create """
        serializer.save(employer=self.request.user)

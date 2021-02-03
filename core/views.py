from core import models, serializers, permissions
from django.contrib.auth import authenticate
from rest_framework import viewsets

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
from django.db.models import Sum


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
    # permission_classes = [permissions.IsAuthenticated]


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


# class ProductViewSet(viewsets.ModelViewSet):
#     """
#     Product serializer
#     """
#     queryset = models.Product.objects.all()
#     serializer_class = serializers.ProductSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class IssueViewSet(viewsets.ModelViewSet):
#     """
#     Issue serializer
#     """
#     queryset = models.Issue.objects.all()
#     serializer_class = serializers.IssueSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class MaterialViewSet(viewsets.ModelViewSet):
#     """
#     Material serializer
#     """
#     queryset = models.Material.objects.all()
#     serializer_class = serializers.MaterialSerializer
#     permission_classes = [permissions.IsAuthenticated]


class ReceiptList(APIView):
    """
    List all receipts, or create a new receipt.
    """
    permission_classes = [permissions.IsOwnerOrReadOnly]

    def get(self, request, format=None):
        material = request.GET.get("material")
        receipts = models.Receipt.objects.filter(employer=request.user)

        total_amount_rice = receipts.filter(
            material=1).aggregate(Sum('total_cost'))
        total_amount_yeast = receipts.filter(
            material=2).aggregate(Sum('total_cost'))

        if material != "":
            receipts = receipts.filter(material=material)

        serializer = serializers.ReceiptSerializer(receipts, many=True)

        return Response({
            "result": serializer.data,
            "total_amount_rice": total_amount_rice["total_cost__sum"],
            "total_amount_yeast": total_amount_yeast["total_cost__sum"]
        })

    def post(self, request, format=None):
        serializer = serializers.ReceiptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReceiptDetail(APIView):
    """
    Retrieve, update or delete a receipt instance.
    """
    permission_classes = [permissions.IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            obj = models.Receipt.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)

            return obj
        except models.Receipt.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        receipt = self.get_object(pk)
        serializer = serializers.ReceiptSerializer(receipt)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        receipt = self.get_object(pk)
        serializer = serializers.ReceiptSerializer(receipt, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        receipt = self.get_object(pk)
        receipt.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderList(APIView):
    """
    List all orders, or create a new order.
    """
    permission_classes = [permissions.IsOwnerOrReadOnly]

    def get(self, request, format=None):
        search = request.GET.get("search")
        orders = models.Order.objects.filter(employer=request.user)
        total_amount = orders.aggregate(Sum('total_cost'))

        orders = orders.filter(customer_name__contains=search)
        serializer = serializers.OrderSerializer(orders, many=True)
        return Response({
            "result": serializer.data,
            "total_amount": total_amount["total_cost__sum"]
        })

    def post(self, request, format=None):
        serializer = serializers.OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):
    """
    Retrieve, update or delete a order instance.
    """
    permission_classes = [permissions.IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            obj = models.Order.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)

            return obj
        except models.Order.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = serializers.OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = serializers.OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        order = self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

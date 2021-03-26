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
import json
from django.core.serializers import serialize as dj_serialize

from rest_framework.decorators import api_view
from notifications.signals import notify

ADMIN_EMAIL = "admin@gmail.com"

ORDER_VERB = {
    "create": "Create Order",
    "update": "Update Order",
    "delete": "Delete Order",
}

RECEIPT_VERB = {
    "create": "Create Receipt",
    "update": "Update Receipt",
    "delete": "Delete Receipt",
}

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

class ReceiptList(APIView):
    """
    List all receipts, or create a new receipt.
    """
    permission_classes = [permissions.IsOwnerOrReadOnly]

    def get(self, request, format=None):
        material = request.GET.get("material")
        receipts = models.Receipt.objects.filter(employer=request.user)
        get_total_info = request.GET.get("get-total-info")

        total_amount_rice = receipts.filter(
            material=1).aggregate(Sum('total_cost'))
        total_amount_yeast = receipts.filter(
            material=2).aggregate(Sum('total_cost'))

        
        # Just get caculated info
        if get_total_info == "all":
            return Response({              
                "total_amount_rice": total_amount_rice["total_cost__sum"],
                "total_amount_yeast": total_amount_yeast["total_cost__sum"]
            })

        # Filters
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
            receipt = serializer.save(employer=request.user)

            admin = models.User.objects.get(email=ADMIN_EMAIL)
            notify.send(sender=request.user, recipient=admin,
                        verb=RECEIPT_VERB["create"], target=receipt, description=serializer.data)
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
        # get old value and send notify
        oldvalue = serializers.ReceiptSerializer(receipt).data

        serializer = serializers.ReceiptSerializer(receipt, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # send notify to admin
            admin = models.User.objects.get(email=ADMIN_EMAIL)
            notify.send(sender=request.user, recipient=admin,
                        verb=RECEIPT_VERB["update"], target=receipt, description={
                            "old": oldvalue,
                            "new": serializer.data
                        })
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        receipt = self.get_object(pk)

        admin = models.User.objects.get(email=ADMIN_EMAIL)
        notify.send(sender=request.user, recipient=admin,
                    verb=RECEIPT_VERB["delete"], target=receipt, description=serializers.ReceiptSerializer(receipt).data)


        receipt.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderList(APIView):
    """
    List all orders, or create a new order.
    """
    permission_classes = [permissions.IsOwnerOrReadOnly]

    def get(self, request, format=None):
        search = request.GET.get("search")
        completed = request.GET.get("completed")
        get_total_info = request.GET.get("get-total-info")

        orders = models.Order.objects.filter(employer=request.user)
        total_amount = orders.aggregate(Sum('total_cost'))
        total_cash = orders.filter(completed=True).aggregate(Sum('total_cost'))


        # Just get caculated info
        if get_total_info == "all":
            return Response({              
                "total_amount": total_amount["total_cost__sum"],
                "total_cash": total_cash["total_cost__sum"]
            })

        # Filters
        orders = orders.filter(customer_name__contains=search)
        if completed == "False":
            orders = orders.filter(completed=False)

        serializer = serializers.OrderSerializer(orders, many=True)
        return Response({
            "result": serializer.data,
            "total_amount": total_amount["total_cost__sum"],
            "total_cash": total_cash["total_cost__sum"]
        })

    def post(self, request, format=None):
        serializer = serializers.OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save(employer=request.user)

            admin = models.User.objects.get(email=ADMIN_EMAIL)
            notify.send(sender=request.user, recipient=admin,
                        verb=ORDER_VERB["create"], target=order, description=serializer.data)
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
        oldvalue = serializers.OrderSerializer(order).data

        serializer = serializers.OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            admin = models.User.objects.get(email=ADMIN_EMAIL)
            notify.send(sender=request.user, recipient=admin,
                        verb=ORDER_VERB["update"], target=order, description={
                            "old": oldvalue,
                            "new": serializer.data
                        })
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        order = self.get_object(pk)

        admin = models.User.objects.get(email=ADMIN_EMAIL)
        notify.send(sender=request.user, recipient=admin,
                    verb=ORDER_VERB["delete"], target=order, description=serializers.OrderSerializer(order).data)

        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def get_notify(request):

    user = request.user
    if user.email == "admin@gmail.com":
        queryset = models.Notification.objects.filter(recipient=user)    
    else:
        queryset = models.Notification.objects.filter(actor_object_id=user.id)
    notify = serializers.NotificationSerializer(queryset, many=True)

    return Response({"result": notify.data})


@api_view()
def get_factory_name(request):

    user = request.user
    queryset = models.User.objects.get(email=user)    

    return Response({"factory_name": user.factory_name})



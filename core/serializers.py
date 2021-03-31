from notifications.base.models import AbstractNotification
from core import models
from rest_framework import serializers
from django.contrib.auth import get_user_model


class LoginSerializer(serializers.Serializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', "factory_name"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', "factory_name"]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"


class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cargo
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = "__all__"


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Material
        fields = "__all__"


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Receipt
        fields = "__all__"


class GenericNotificationRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        if isinstance(value, models.Order):
            serializer = OrderSerializer(value)
        if isinstance(value, models.Receipt):
            serializer = ReceiptSerializer(value)
        if isinstance(value, models.Cargo):
            serializer = CargoSerializer(value)

        return serializer.data

class GenericNotificationRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        if isinstance(value, models.Order):
            serializer = OrderSerializer(value)
        if isinstance(value, models.Receipt):
            serializer = ReceiptSerializer(value)
        if isinstance(value, models.Cargo):
            serializer = CargoSerializer(value)

        return serializer.data


class NotificationSerializer(serializers.Serializer):
    recipient = UserSerializer(models.User, read_only=True)
    actor = UserSerializer(models.User, read_only=True)
    unread = serializers.BooleanField(read_only=True)
    verb = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    target = GenericNotificationRelatedField(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)

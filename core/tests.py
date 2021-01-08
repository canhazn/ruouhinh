from django.shortcuts import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from core import models

RECEIPT_URL = reverse('core_api:receipt-list')
TOKEN_URL = reverse('core_api:token')


def create_user(**params):
    return User.objects.create_user(**params)


class UserTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def sample_receipt(user, material, **params):
        """Create and return a sample receipt"""
        defaults = {
            'quantity': 2,
            'total-cost': 100000,
        }
        defaults.update(params)

        return models.Receipt.objects.create(employer=user, material=material, **defaults)


class ReceiptTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="test-user",
            password="123456"
        )
        self.client.force_authenticate(user=self.user)

    def test_view_receipt(self):
        response = self.client.get(RECEIPT_URL, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_basic_recipet(self):
        """Test creating receipt"""

        material = models.Material.objects.create(
            title="Gạo", description="gao xay")

        payload = {
            "material": material.id,
            "quantity": 3,
            "total_cost": 2
        }
        res = self.client.post(RECEIPT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        receipt = models.Receipt.objects.get(id=res.data['id'])
        for key in payload.keys():
            if key == "material":
                self.assertEqual(material, getattr(receipt, key))
            else:
                self.assertEqual(payload[key], getattr(receipt, key))

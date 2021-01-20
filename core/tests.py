from django.shortcuts import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from core import models

RECEIPT_URL = reverse('core_api:receipt-list')


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


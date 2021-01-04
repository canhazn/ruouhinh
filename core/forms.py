from django import forms
from product import models


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        exclude = ('delivered', )

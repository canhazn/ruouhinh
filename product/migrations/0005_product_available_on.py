# Generated by Django 3.0.6 on 2020-09-02 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_product_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='available_on',
            field=models.TextField(blank=True, max_length=10, null=True),
        ),
    ]

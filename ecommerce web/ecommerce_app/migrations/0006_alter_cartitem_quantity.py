# Generated by Django 5.1.1 on 2024-09-09 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0005_remove_cart_product_remove_cart_quantity_cartitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
# Generated by Django 4.1.7 on 2023-03-17 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0029_activated_customer_name_cart_customer_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='old_price',
            field=models.IntegerField(null=True),
        ),
    ]

# Generated by Django 4.1.7 on 2023-03-15 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0024_alter_cart_color_alter_cart_number_alter_cart_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='product',
            field=models.IntegerField(null=True),
        ),
    ]
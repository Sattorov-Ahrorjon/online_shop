# Generated by Django 4.1.7 on 2023-03-15 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0021_alter_cart_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='customer',
            field=models.IntegerField(null=True),
        ),
    ]
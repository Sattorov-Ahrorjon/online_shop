from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify
from account.models import Customer


class Status(models.TextChoices):
    Draft = "DF" "Draft"
    Published = "PB" "Published"


class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, editable=False)

    def save(self, *args, **kwargs):
        var = self.name
        self.slug = slugify(var, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Size(models.Model):
    symbol = models.CharField(max_length=15)
    number = models.IntegerField()

    def __str__(self):
        return f"{self.symbol} - {self.number}"


class Color(models.Model):
    color = models.CharField(max_length=200)

    def __str__(self):
        return self.color


class Product(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, editable=False)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    body = models.TextField()
    image = models.ImageField(upload_to='images/', verbose_name='Image (width and height should be equal)')
    created_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.Draft
    )

    class Meta:
        ordering = ['-created_time']

    def save(self, *args, **kwargs):
        var = self.name
        self.slug = slugify(var, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Comment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    star = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return self.body


class Filter(models.Model):
    customer = models.CharField(max_length=150, unique=True)
    number = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    color = models.CharField(max_length=200, null=True, blank=True)
    size = models.CharField(max_length=15, null=True, blank=True)
    category = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.number


class AveragePrice(models.Model):
    price = models.IntegerField()

    def __str__(self):
        return str(self.price)


class Cart(models.Model):
    customer = models.IntegerField(null=True)
    customer_name = models.CharField(max_length=150, null=True)
    product = models.IntegerField(null=True)
    product_name = models.CharField(max_length=150, null=True)
    price = models.IntegerField(null=True)
    size = models.CharField(max_length=15, null=True)
    color = models.CharField(max_length=100, null=True)
    number = models.IntegerField(null=True)
    summ = models.IntegerField(null=True)
    added_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-added_time']

    def __str__(self):
        return self.product_name


class Activated(models.Model):
    customer = models.IntegerField(null=True)
    customer_name = models.CharField(max_length=150, null=True)
    product = models.IntegerField(null=True)
    product_name = models.CharField(max_length=150, null=True)
    delivery_time = models.DateTimeField(null=True, blank=True)
    country = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    street = models.CharField(max_length=150)
    house_number = models.CharField(max_length=150)
    payment_method = models.CharField(max_length=150, null=True, blank=True)  # null blank del

    class Meta:
        ordering = ['delivery_time']

    def __str__(self):
        return self.product_name


class Purchased(models.Model):
    customer = models.IntegerField(null=True)
    customer_name = models.CharField(max_length=150, null=True)
    product = models.IntegerField(null=True)
    product_name = models.CharField(max_length=150, null=True)
    created_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return self.product_name

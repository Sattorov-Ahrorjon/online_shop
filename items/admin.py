from django.contrib import admin
from .models import (
    Product,
    Category,
    Status,
    Comment,
    Color,
    Size,
    Filter,
    AveragePrice,
    Cart,
    Purchased,
    Activated,
)


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['id', 'name', 'created_time', 'status']
    list_display_links = ['name']
    actions = ['published', 'draft']

    def published(self, request, queryset):
        queryset.update(status=Status.Published)

    def draft(self, request, queryset):
        queryset.update(status=Status.Draft)


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['id', 'name']
    list_display_links = ['name']


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['id', 'customer', 'product', 'star', 'active']
    list_display_links = ['customer']
    actions = ['disable_comment', 'activate_comment']

    def disable_comment(self, request, queryset):
        queryset.update(active=False)

    def activate_comment(self, request, queryset):
        queryset.update(active=True)


class ColorAdmin(admin.ModelAdmin):
    list_display = ['id', 'color']
    list_display_links = ['color']


class SizeAdmin(admin.ModelAdmin):
    list_display = ['id', 'symbol', 'number']
    list_display_links = ['symbol']


class FilterAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'number', 'price', 'color', 'size', 'category']
    list_display_links = ['customer']


class AveragePriceAdmin(admin.ModelAdmin):
    list_display = ['id', 'price']
    list_display_links = ['price']


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'product_name', 'price', 'summ', 'size', 'color', 'number', 'added_time']
    list_display_links = ['product_name']


class PurchasedAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'product_name', 'created_time']
    list_display_links = ['product_name']


class ActivatedAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'product_name', 'delivery_time', 'country', 'city', 'street', 'house_number']
    list_display_links = ['product_name']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Filter, FilterAdmin)
admin.site.register(AveragePrice, AveragePriceAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Purchased, PurchasedAdmin)
admin.site.register(Activated, ActivatedAdmin)

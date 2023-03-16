from django.urls import path
from .views import *


urlpatterns = [
    path('', get_home, name='home_page'),
    path('shop/', get_shop, name='shop_page'),
    path('detail/<slug:slug>/<int:idd>/', get_detail, name='detail_page'),
    path('save-comment/<slug:slug>/<int:idd>/', save_comment, name='save_comment'),
    path('save-product/', save_product, name='save_product'),
    path('remove-product/<int:idd>/', remove_product, name='remove_product'),
    path('cart/', get_cart, name='cart_page'),
    path('checkout/', get_checkout, name='checkout_page'),
    path('shop/ordered-store/<int:number>/', get_sorting_store, name='ordered_store'),
    path('shop/ordered-store/category/<slug:category>/', get_sorting_category, name='get_category_sort_page'),
    path('shop/ordered-store/price/<int:price>/', get_sorting_price, name='ordered_store_price'),
    path('shop/ordered-store/color/<str:color>/', get_sorting_color, name='ordered_store_color'),
    path('shop/ordered-store/size/<str:size>/', get_sorting_size, name='ordered_store_size'),
    path('product/payment/', get_payment, name='payment'),
]

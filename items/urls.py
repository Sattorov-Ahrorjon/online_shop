from django.urls import path
from .views import *


urlpatterns = [
    path('', get_home_view, name='home_page'),
    path('shop/', get_shop_view, name='shop_page'),
    path('detail/<slug:slug>/<int:idd>/', get_detail_view, name='detail_page'),
    path('save-comment/<slug:slug>/<int:idd>/', save_comment_view, name='save_comment'),
    path('save-product/', save_product_view, name='save_product'),
    path('remove-product/<int:idd>/', remove_product_view, name='remove_product'),
    path('cart/', get_cart_view, name='cart_page'),
    path('checkout/', get_checkout_view, name='checkout_page'),
    path('shop/ordered-store/<int:number>/', get_sorting_store_view, name='ordered_store'),
    path('shop/ordered-store/category/<slug:category>/', get_sorting_category_view, name='get_category_sort_page'),
    path('shop/ordered-store/price/<int:price>/', get_sorting_price_view, name='ordered_store_price'),
    path('shop/ordered-store/color/<str:color>/', get_sorting_color_view, name='ordered_store_color'),
    path('shop/ordered-store/size/<str:size>/', get_sorting_size_view, name='ordered_store_size'),
    path('product/payment/', get_payment_view, name='payment'),
]

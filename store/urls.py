from django.urls import path

from .views import products_view
from .views import shop_view
from .views import products_page_view
from .views import cart_view
from .views import cart_add_view
from .views import cart_del_view
from .views import coupon_check_view
from .views import delivery_estimate_view
from .views import cart_buy_now_view
from .views import cart_remove_view

app_name = 'store'

urlpatterns = [
    path('product/', products_view),
    path('', shop_view, name="shop_view"),
    path('product/<slug:page>.html', products_page_view, name="products_page_view"),
    path('product/<int:page>', products_page_view),
    path('cart/', cart_view, name="cart_view"),
    path('cart/add/<str:id_product>', cart_add_view),
    path('cart/del/<str:id_product>', cart_del_view),
    path('coupon/check/<slug:name_coupon>', coupon_check_view),
    path('delivery/estimate', delivery_estimate_view),
    path('cart/buy/<str:id_product>', cart_buy_now_view, name="buy_now"),
    path('cart/remove/<str:id_product>', cart_remove_view, name="remove_now"),
]

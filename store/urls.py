from django.urls import path

from .views import products_view
from .views import shop_view
from .views import products_page_view


urlpatterns = [
    path('product/', products_view),
    path('', shop_view),
    path('product/<slug:page>.html', products_page_view),
    path('product/<int:page>', products_page_view),
]

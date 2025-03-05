from django.urls import path
from orders.views import cart, checkout, processOrder, updateItem
from django.views.generic import TemplateView


app_name = 'orders'
urlpatterns = [
    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),
    path('update_item/', updateItem, name="update_item"),
    path('process_order/', processOrder, name="process_order"),
]

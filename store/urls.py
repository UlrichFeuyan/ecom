from django.urls import path
from .views import *
from django.views.generic import TemplateView


app_name = 'store'
urlpatterns = [
    path('', index, name='index'),
    path('store', store, name='store'),
    path('search/', search, name="search"),
    path('produit/<str:slug>/', product_detail, name="detail"),
    path('add/', product_add, name='product_add'),
    path('categorie_produit/<str:category>/', listing_by_category, name="categorie_produit"),

    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),

    path('update_item/', updateItem, name="update_item"),
    path('process_order/', processOrder, name="process_order"),
]


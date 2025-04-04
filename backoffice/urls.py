from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from django.urls import path, include

from backoffice.views import products, customers, categories, orders, suppliers


app_name = 'backoffice'
urlpatterns = [
    # produits
    path('products/', products.products, name="products"),
    
    path('get_add_product_form/', products.get_add_product_form, name="get_add_product_form"),
    path('get_view_product/<str:slug>/', products.get_view_product, name="get_view_product"),
    path('get_edit_product_form/<str:slug>/', products.get_edit_product_form, name="get_edit_product_form"),
    path('get_delete_product_form/<str:slug>/', products.get_delete_product_form, name="get_delete_product_form"),
    
    path('product_add/', products.product_add, name="product_add"),
    path('product_update/<str:slug>/', products.product_update, name="product_update"),
    path('product_delete/<str:slug>/', products.product_delete, name="product_delete"),
    
    
    # Catégories
    
    
    # Clients
    
    
    # Commandes
    
    
    # fournisseurs
    
]

from django.urls import path
from products.views import *
from django.views.generic import TemplateView


app_name = 'products'
urlpatterns = [
    path('produc/list/', product_list, name='list'),
    path('product/detail/<str:slug>/', product_detail, name="detail"),
    path('product/update/<str:slug>/', product_update, name="update"),
    path('product/add/', product_detail, name="add"),
    path('product/delete/<str:slug>/', product_delete, name="delete"),
    path('product/search/', product_search, name="search"),
    path('product/filter/', product_filter, name='filter'),
]


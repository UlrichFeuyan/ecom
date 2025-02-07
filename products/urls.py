from django.urls import path
from products.views import *
from django.views.generic import TemplateView


app_name = 'products'
urlpatterns = [
    path('list/', product_list, name='list'),
    path('detail/<str:slug>/', product_detail, name="detail"),
    path('update/<str:slug>/', product_update, name="update"),
    path('add/', product_detail, name="add"),
    path('delete/<str:slug>/', product_delete, name="delete"),
    path('search/', product_search, name="search"),
    path('instant_search_suggests/', instant_search_suggests, name="instant_search_suggests"),
    path('filter/', product_filter, name='filter'),
]


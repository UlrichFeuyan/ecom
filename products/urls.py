from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import *
from django.views.generic import TemplateView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products_api')


app_name = 'products'
urlpatterns = [
    path('list/', product_list, name='list'),
    path('detail/<str:slug>/', product_detail, name="detail"),
    path('search/', product_search, name="search"),
    path('instant_search_suggests/', instant_search_suggests, name="instant_search_suggests"),
    path('filter/', product_filter, name='filter'),
    
    # gestion des produits
    path('api/', include(router.urls)),
    path('get_add_product_form/', get_add_product_form, name="get_add_product_form"),
    path('product_add/', product_add, name="product_add"),
    path('update/<str:slug>/', product_update, name="update"),
    path('delete/<str:slug>/', product_delete, name="delete"),
    path('manage/products', products, name='products'),
]


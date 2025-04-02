from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backoffice.views import *
from django.views.generic import TemplateView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products_api')


app_name = 'backoffice'
urlpatterns = [
    path('api/', include(router.urls)),
    path('get_add_product_form/', get_add_product_form, name="get_add_product_form"),
    path('get_view_product/<str:slug>/', get_view_product, name="get_view_product"),
    path('get_edit_product_form/<str:slug>/', get_edit_product_form, name="get_edit_product_form"),
    path('get_delete_product_form/<str:slug>/', get_delete_product_form, name="get_delete_product_form"),
    path('product_add/', product_add, name="product_add"),
    path('view/<str:slug>/', product_view, name="update"),
    path('update/<str:slug>/', product_update, name="update"),
    path('delete/<str:slug>/', product_delete, name="delete"),
    path('products', products, name='products'),
]

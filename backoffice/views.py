from django.shortcuts import redirect, render, get_object_or_404
from rest_framework import viewsets
from django.contrib import messages
from django.db import transaction
import sweetify

from backoffice.pagination import CustomDatatablesPagination, DatatablesPagination
from backoffice.serializers import ProductSerializer
from products.forms import ProductDeleteForm, ProductForm
from products.models import Product, ProductImage


# 
# Dashbord
# 

def dashbord(request):
    dashbord_active = "true"
    return render(request, "backoffice/dashbord.html", locals())


# 
# Product
# 


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomDatatablesPagination # Active la pagination DataTables


def products(request):
    products_active = "true"
    return render(request, "backoffice/products.html", locals())

def get_add_product_form(request):
    form = ProductForm()
    return render(request, 'products/product_add_form.html', locals())

def get_view_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'products/product_view.html', locals())

def get_edit_product_form(request, slug):
    product = get_object_or_404(Product, slug=slug)
    slug = slug
    # form = ProductForm(request.POST)
    return render(request, 'products/product_edit_form.html', locals())

def get_delete_product_form(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'products/product_delete.html', locals())
    
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        images = request.FILES.getlist('images')

        if form.is_valid():
            try:
                with transaction.atomic():  # Assurer une atomicité
                    product = form.save()

                    # Enregistrer chaque image associée au produit
                    for image in images:
                        ProductImage.objects.create(produit=product, thumbnail=image)

                sweetify.success(request, "Produit ajouté avec succès !", timer=2000, toast=True, timerProgressBar=True, position="top")
                return redirect('products:products')

            except Exception as e:
                sweetify.info(request, f"Erreur lors de l'ajout du produit : {str(e)} !", timer=2000, toast=True, timerProgressBar=True, position="top")
                return redirect('products:products')
        else:
            sweetify.info(request, "Erreur lors de l'ajout du produit !", timer=2000, toast=True, timerProgressBar=True, position="top")
            return redirect('products:products')
  
    messages.success(request, "Erreur lors de l'ajout du produit !")
    return redirect('products:products')

def product_view(request, pk):
    pass

def product_update(request, pk):
    pass

def product_delete(request, pk):
    pass


# 
# Dashbord
# 

def categories(request):
    categories_active = "true"
    return render(request, "backoffice/categories.html", locals())


# 
# Dashbord
# 

def customers(request):
    customers_active = "true"
    return render(request, "backoffice/customers.html", locals())


# 
# Dashbord
# 

def supliers(request):
    supliers_active = "true"
    return render(request, "backoffice/supliers.html", locals())


# 
# Dashbord
# 

def orders(request):
    orders_active = "true"
    return render(request, "backoffice/orders.html", locals())

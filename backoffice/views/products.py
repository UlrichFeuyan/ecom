from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
import sweetify

from products.models import Category, Marque, Product, ProductImage, Tag
from products.forms import ProductForm


def products(request):
    menu_product = "True"
    list_products = "True"
    
    table_size = request.GET.get("table_size")
    search_text = request.GET.get("search_text")
    
    products = Product.objects.all()
    
    if not search_text:
        pass
    else:
        products = Product.objects.filter(name__icontains=search_text)
        if not products.exists():
            products = Product.objects.filter(description__icontains=search_text)
        if not products.exists():
            products = Product.objects.filter(category__name__icontains=search_text)
        if not products.exists():
            products = Product.objects.filter(marque__name__icontains=search_text)
        if not products.exists():
            products = Product.objects.filter(tag__name__icontains=search_text)
    
    
    paginator = Paginator(products, table_size if table_size else 5)

    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
        
    return render(request, "products/products.html", locals())

def get_add_product_form(request):
    form = ProductForm()
    return render(request, 'products/product_add_form.html', locals())

def get_view_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'products/product_view.html', locals())

def get_edit_product_form(request, slug):
    product = get_object_or_404(Product, slug=slug)
    tags = Tag.objects.all()
    categories = Category.objects.all()
    marques = Marque.objects.all()
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

def product_update(request, slug):
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

def product_delete(request, slug):
    pass

from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from products.pagination import CustomDatatablesPagination
from products.serializers import ProductSerializer
from products.forms import ProductForm, ProductImageForm, ProductImageFormSet
from products.models import Category, Product, ProductImage
from rest_framework import viewsets
from django.contrib import messages
from django.db import transaction
from store.utils import cookieCart, cartData, guestOrder
import sweetify


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomDatatablesPagination  # Active la pagination DataTables

def product_list(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    categories = Category.objects.all()
    paginator = Paginator(products, 6)

    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request, "products/product_list.html", locals())

def products(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    categories = Category.objects.all()
    paginator = Paginator(products, 6)

    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request, "products/products.html", locals())

def product_detail(request, slug):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    categories = Category.objects.all()
    product = get_object_or_404(Product, slug=slug)
    return render(request, "products/product_detail.html", locals())

def get_add_product_form(request):
    form = ProductForm()
    return render(request, 'products/product_form.html', locals())

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

def product_update(request, pk):
    pass

def product_delete(request, pk):
    pass

def product_filter(request):
    pass

def product_search(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories = Category.objects.all()

    query = request.GET.get('query')
    page_title = "Résultats"
    page_title_detail = f"Résultats de la recherche \"{query}\""

    if not query:
        return redirect(request.META['HTTP_REFERER'])  # Actualise la page
    else:
        products = Product.objects.filter(name__icontains=query)
    if not products.exists():
        products = Product.objects.filter(description__icontains=query)
    if not products.exists():
        products = Product.objects.filter(category__name__icontains=query)
    if not products.exists():
        products = Product.objects.filter(marque__name__icontains=query)
    if not products.exists():
        products = Product.objects.filter(tag__name__icontains=query)

    paginator = Paginator(products, 6)

    page_num = request.GET.get('page')
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request, 'products/product_list.html', locals())

def instant_search_suggests(request):
    products = Product.objects.all()
    query = request.GET.get('query')
    if not query:
        no_result = "..."
        products = None
        return render(request, 'products/product_instant_search_suggests.html', locals())
    else:
        products = Product.objects.filter(name__icontains=query)
    if not products.exists():
        products = Product.objects.filter(description__icontains=query)
    if not products.exists():
        products = Product.objects.filter(category__name__icontains=query)
    if not products.exists():
        products = Product.objects.filter(marque__name__icontains=query)
    if not products.exists():
        products = Product.objects.filter(tag__name__icontains=query)
    
    return render(request, 'products/product_instant_search_suggests.html', locals())

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    categories = Category.objects.all()

    return render(request, 'store/cart.html', locals())


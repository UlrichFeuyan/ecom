from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from products.forms import ProductForm, ProductImageFormSet
from products.models import Category, Product, ProductImage
from django.db import transaction
from store.utils import cookieCart, cartData, guestOrder


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

def product_detail(request, slug):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    categories = Category.objects.all()
    product = get_object_or_404(Product, slug=slug)
    return render(request, "products/product_detail.html", locals())

def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        formset = ProductImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                product = form.save()
                images = formset.save(commit=False)
                for image in images:
                    image.produit = product
                    image.save()

                messages.success(request, "Produit ajouté avec succès !")
                return redirect('products:add_product')

    else:
        form = ProductForm()
        formset = ProductImageFormSet()

    return render(request, 'products/product_form.html', {'form': form, 'formset': formset})

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


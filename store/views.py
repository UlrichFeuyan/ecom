from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from orders.models import Order, OrderItem, ShippingAddress
from products.forms import ProductForm, ProductImageFormSet
from products.models import Category, Product, ProductImage
from django.http import JsonResponse
from django.db import transaction
from store.utils import cookieCart, cartData, guestOrder
import json
import datetime


def index(request):
    top_bar = True
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

    return render(request, "store/home.html", locals())


def store(request):
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

    return render(request, "store/store.html", locals())


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    categories = Category.objects.all()

    return render(request, 'store/cart.html', locals())


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories = Category.objects.all()

    return render(request, 'store/checkout.html', locals())


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']

    action = data['action']

    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    categories = Category.objects.all()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)


def listing(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    paginator = Paginator(products, 3)

    page_num = request.GET.get('page')
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return render(request, 'store/listing.html', locals())


def listing_by_category(request, category):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.filter(category__name=category).order_by()
    categories = Category.objects.all()
    paginator = Paginator(products, 6)

    title = f"Produits de la categorie : \"{category}\""

    page_num = request.GET.get('page')
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    context = {'page': page,
               'paginate': True,
               }
    return render(request, 'store/categorie_produit.html', locals())


def search(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories = Category.objects.all()

    query = request.GET.get('query')
    title = f"Résultats de la recherche \"{query}\""

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

    paginator = Paginator(products, 6)

    page_num = request.GET.get('page')
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request, 'store/search.html', locals())


def product_detail(request, slug):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    categories = Category.objects.all()
    product = get_object_or_404(Product, slug=slug)
    return render(request, "store/detail_n.html", locals())

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
                return redirect('store:product_add')

    else:
        form = ProductForm()
        formset = ProductImageFormSet()

    return render(request, 'store/product_form.html', {'form': form, 'formset': formset})

def error_404(request, exception):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories = Category.objects.all()
    return render(request, '404.html', locals())


def error_500(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories = Category.objects.all()
    return render(request, '500.html', locals())


def apropos(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    categories = Category.objects.all()
    return render(request, 'apropos.html', locals())


def faq(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories = Category.objects.all()
    return render(request, 'FAQ.html', locals())


def contact(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories = Category.objects.all()
    return render(request, 'contact.html', locals())

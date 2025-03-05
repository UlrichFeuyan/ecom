from products.utils import cartData
from products.models import Category

def cart_context(request):
    """Ajoute les données du panier et les catégories à chaque template."""
    data = cartData(request)

    return {
        'cartItems': data['cartItems'],
        'order': data['order'],
        'items': data['items'],
        'categories': Category.objects.all()
    }

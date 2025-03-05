from django.utils.functional import SimpleLazyObject
from products.utils import cartData

class CartMiddleware:
    """Middleware pour ajouter les données du panier à chaque requête."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Ajoute le panier à la requête avant le traitement."""
        request.cart_data = SimpleLazyObject(lambda: cartData(request))
        response = self.get_response(request)
        return response

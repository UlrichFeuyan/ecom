from rest_framework import serializers
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    marque_name = serializers.CharField(source='marque.name', read_only=True)
    tags = serializers.SerializerMethodField()
    first_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'category_name', 'marque_name', 'tags', 'price', 'stock', 'first_image']
        
    def get_price(self, obj):
        return obj.price if obj.price else 0
    
    def get_stock(self, obj):
        return obj.stock if obj.stock else 0
    
    def get_category_name(self, obj):
        return obj.category.name if obj.category else "Non catégorisé"

    def get_marque_name(self, obj):
        return obj.marque.name if obj.marque else "Sans marque"

    def get_tags(self, obj):
        """ Récupère tous les tags sous forme de liste """
        return [tag.name for tag in obj.tag.all()] if obj.tag.exists() else ["Aucun Tag"] # ManyToManyField -> liste de tags

    def get_first_image(self, obj):
        """ Récupère la première image du produit ou une image par défaut """
        first_image = obj.get_first_image()
        if first_image:
            return first_image.thumbnail.url
        return "/static/images/placeholder.png"  # Image par défaut

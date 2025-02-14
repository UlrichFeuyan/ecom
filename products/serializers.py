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

    def get_tags(self, obj):
        """ Récupère tous les tags sous forme de liste """
        return [tag.name for tag in obj.tag.all()]  # ManyToManyField -> liste de tags

    def get_first_image(self, obj):
        """ Récupère la première image du produit ou une image par défaut """
        first_image = obj.get_first_image()
        if first_image:
            return first_image.thumbnail.url
        return "/static/assets/img/placeholder.png"  # Image par défaut

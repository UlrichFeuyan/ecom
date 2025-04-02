import os
from django.db import models
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


def img_path_categories(instance, filename):
    path = "categories/"
    path += instance.name + "/"
    return os.path.join(path, filename)


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField("Photo du produit", upload_to=img_path_categories)

    class Meta:
        verbose_name = "Categorie"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
    def visuel(self):
        if self.image.url :
            return mark_safe('<img src="{}" alt="{}" width="100" />'.format(self.image.url, self.name))
        return mark_safe('<img src="{}" alt="{}" width="100" />'.format("/static/images/placeholder.png", self.name))

    visuel.allow_tags = True


class Marque(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Marque"
        verbose_name_plural = "Marques"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("Nom du produit", max_length=255)
    slug = models.SlugField("Slug", max_length=255, unique=True)
    price = models.IntegerField("Prix", default=0)
    category = models.ForeignKey(Category, verbose_name="Catégorie", on_delete=models.DO_NOTHING, blank=True, null=True)
    tag = models.ManyToManyField(Tag, verbose_name="Tag", related_name="products", blank=True, through='ProductTag')
    marque = models.ForeignKey(Marque, blank=True, null=True, on_delete=models.DO_NOTHING)
    stock = models.IntegerField("Quantité en stock", default=0)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "produits"

    def __str__(self):
        return f"{self.name} ({self.stock})"

    def get_absolute_url(self):
        return reverse('store:detail', kwargs={"slug": self.slug})

    def get_all_images(self):
        return ProductImage.objects.filter(produit=self)

    def get_first_image(self):
        try:
            return ProductImage.objects.filter(produit=self)[0]
        except IndexError:
            return None

    def get_second_image(self):
        try:
            return ProductImage.objects.filter(produit=self)[1]
        except IndexError:
            return None
        
    def get_all_tags(self):
        return Tag.objects.filter(produit=self)
        
    def visuel(self):
        return mark_safe('<img src="{}" alt="{}" width="100" />'.format(self.get_first_image().thumbnail.url, self.name))

    visuel.allow_tags = True


class ProductTag(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('product', 'tag')  # Éviter les doublons
        verbose_name = "Relation Produit-Tag"
        verbose_name_plural = "Relations Produit-Tag"

    def __str__(self):
        return f"{self.product.name} - {self.tag.name}"


def img_path_products(instance, filename):
    path = "products/"
    path += instance.produit.name + "/"
    
    if instance.produit.category:
        path += instance.produit.category.name + "/"
    return os.path.join(path, filename)


class ProductImage(models.Model):
    produit = models.ForeignKey(Product, related_name='photos', on_delete=models.CASCADE)
    thumbnail = models.ImageField("Photo du produit", upload_to=img_path_products)

    class Meta:
        verbose_name = "photo de Produit"
        verbose_name_plural = "photos de produit"

    def __str__(self):
        return self.produit.name

    def visuel(self):
        return mark_safe(
            '<img src="{}" alt="{}" width="100" height="100" />'.format(self.thumbnail.url, self.produit.name))

    visuel.allow_tags = True

    @property
    def thumbnailURL(self):
        try:
            url = self.thumbnail.url
        except:
            url = "/static/assets/img/placeholder.png"
        return url


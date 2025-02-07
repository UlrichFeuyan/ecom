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


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Categorie"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Marque(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Marque"
        verbose_name_plural = "Marques"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("Nom du produit", max_length=255)
    slug = models.SlugField("Slug", max_length=255)
    price = models.IntegerField("Prix", default=0)
    category = models.ForeignKey(Category, verbose_name="Catégorie", on_delete=models.CASCADE, blank=True, null=True)
    tag = models.ManyToManyField(Tag, verbose_name="Tag", related_name="products", blank=True)
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE, blank=True, null=True)
    stock = models.IntegerField("Quantité en stock", default=0)
    description = RichTextField(verbose_name="Description", blank=True, null=True)

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
        
    def visuel(self):
        return mark_safe('<img src="{}" alt="{}" width="100" />'.format(self.get_first_image().thumbnail.url, self.name))

    visuel.allow_tags = True


def img_path_products(instance, filename):
    path = "products/"
    ext = filename.split('.')[-1] # Extension du fichier (Sera convertis vers un type défini si nécessaire)
    
    # Les images des produits seront classées dans un répertoire portant le 
    # nom du produit et ce répertoire sera dans le répertoire de associé
    # à sa catégorie
    if instance.produit.category:
        path += instance.produit.name + "/"
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


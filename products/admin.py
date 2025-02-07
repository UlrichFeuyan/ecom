from django.contrib import admin
from products.models import Category, Marque, Product, ProductImage, Tag


admin.site.register(Tag)
admin.site.register(Marque)

class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    verbose_name = "Produit"
    verbose_name_plural = "Produits"


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    verbose_name = "Photo"
    verbose_name_plural = "Photos"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ]
    list_display = ['name', 'category', 'marque', 'visuel']
    list_filter = ['category', 'marque', 'tag']
    search_fields = ['name', 'category', 'marque']
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategorieAdmin(admin.ModelAdmin):
    inlines = [ProductInline, ]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['produit', 'visuel']
    list_filter = ['produit']
    list_per_page = 12
    list_max_show_all = 20

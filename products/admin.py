from django.contrib import admin
from django.forms import CharField, ModelForm
from ckeditor_uploader.widgets import CKEditorUploadingWidget
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



class ProductAdminForm(ModelForm):
    description = CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Product
        fields = '__all__'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ]
    list_display = ['name', 'category', 'marque', 'visuel']
    list_filter = ['category', 'marque', 'tag']
    search_fields = ['name', 'category', 'marque', 'description']
    prepopulated_fields = {"slug": ("name",)}
    form = ProductAdminForm


@admin.register(Category)
class CategorieAdmin(admin.ModelAdmin):
    inlines = [ProductInline, ]
    list_display = ['name', 'visuel']
    search_fields = ['name']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['produit', 'visuel']
    list_filter = ['produit']
    list_per_page = 12
    list_max_show_all = 20

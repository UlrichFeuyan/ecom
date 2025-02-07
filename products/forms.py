from django.forms import CharField, ClearableFileInput, FileField, ModelForm, DateInput, NumberInput, Select, SelectMultiple, TextInput, Textarea, inlineformset_factory, modelformset_factory
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper, AdminFileWidget
from products.models import ProductImage, Product, Marque, Category, Tag
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextFormField
from django.urls import reverse
from datetime import datetime


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class MarqueForm(ModelForm):
    class Meta:
        model = Marque
        fields = '__all__'


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'


class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'slug', 'price', 'category', 'tag', 'marque', 'stock', 'description']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'slug': TextInput(attrs={'class': 'form-control'}),
            'price': NumberInput(attrs={'class': 'form-control'}),
            'category': Select(attrs={'class': 'form-control'}),
            'tag': SelectMultiple(attrs={'class': 'form-control'}),
            'marque': Select(attrs={'class': 'form-control'}),
            'stock': NumberInput(attrs={'class': 'form-control'}),
            'description': RichTextFormField(config_name="default"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ajout dynamique de boutons "Ajouter" pour les catégories, tags, marques
        for field_name in ['category', 'tag', 'marque']:
            self.fields[field_name].widget = RelatedFieldWidgetWrapper(
                self.fields[field_name].widget,
                self._meta.model._meta.get_field(field_name).remote_field,  # ✅ Correction ici
                reverse(f'admin:{self._meta.model._meta.app_label}_{field_name}_add'),  # ✅ Correction ici
                False,
            )

class ProductImageForm(ModelForm):
    class Meta:
        model = ProductImage
        fields = ['thumbnail']
        widgets = {
            'thumbnail': AdminFileWidget,  # Utilisation du widget admin pour l'upload
        }

ProductImageFormSet = inlineformset_factory(
    Product, ProductImage,
    form=ProductImageForm,
    extra=1,  # Minimum une image
    can_delete=True
)
    
    
    
    
        # labels = {
        #     'name': _("Nom"),
        #     'price': _("Prix"),
        #     'category': _("Catégorie"),
        #     'marque': _("Marque"),
        #     'tag': _("Tag(s)"),
        #     'stock': _("Quantité en stock"),
        #     'description': _("Description"),
        # }
        # widgets = {
        #     'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du produit', 'type': 'text'}),
        #     'departement': Select(attrs={'class': 'form-control', 'placeholder': 'Département'}),
        #     'poste': TextInput(attrs={'class': 'form-control', 'placeholder': 'Poste Occupé', 'type': 'text'}),
        #     'ncni': TextInput(attrs={'class': 'form-control', 'placeholder': 'Numéro de cni', 'type': 'text'}),
        #     'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du produit', 'type': 'text'}),
        #     'departement': Select(attrs={'class': 'form-control', 'placeholder': 'Département'}),
        #     'poste': TextInput(attrs={'class': 'form-control', 'placeholder': 'Poste Occupé', 'type': 'text'}),
        #     'ncni': TextInput(attrs={'class': 'form-control', 'placeholder': 'Numéro de cni', 'type': 'text'}),
        #     # 'date_naissance': DateInput(format=('%d/%m/%Y'), attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date', 'min': '1940-01-01', 'max': '2012-12-31'}),
        # }

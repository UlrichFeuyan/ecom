from django.forms import CharField, ClearableFileInput, FileField, FileInput, ModelForm, DateInput, ModelMultipleChoiceField, NumberInput, Select, SelectMultiple, TextInput, Textarea, inlineformset_factory, modelformset_factory
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
    tag = ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=SelectMultiple(attrs={'class': 'tf-field-input tf-input'}),
        required=False,
        label=_("Tags")
    )

    class Meta:

        model = Product
        fields = ['name', 'slug', 'price', 'category', 'tag', 'marque', 'stock', 'description']
        
        labels = {
            'name': _("Nom du produit"),
            'slug': _("Slug"),
            'price': _("Prix"),
            'category': _("Catégorie"),
            'tag': _("Tags"),
            'marque': _("Marque"),
            'stock': _("Quantité en stock"),
            'description': _("Description"),
        }

        widgets = {
            'name': TextInput(attrs={'class': 'tf-field-input tf-input'}),
            'slug': TextInput(attrs={'class': 'tf-field-input tf-input', 'required': 'required'}),
            'price': NumberInput(attrs={'class': 'tf-field-input tf-input', 'min': 0}),
            'category': Select(attrs={'class': 'tf-select w-100'}),
            'marque': Select(attrs={'class': 'tf-select w-100'}),
            'stock': NumberInput(attrs={'class': 'tf-field-input tf-input', 'min': 0}),
            'description': Textarea(attrs={'class': 'tf-field-input tf-input', 'rows': 4}),
        }


class ProductImageForm(ModelForm):
    class Meta:
        model = ProductImage
        fields = ['thumbnail']
        widgets = {
            'thumbnail': FileInput(attrs={'class': 'form-control'}),
        }

ProductImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=3)

    
    
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

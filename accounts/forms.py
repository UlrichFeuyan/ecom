from crispy_forms.bootstrap import PrependedText, FormActions
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.forms import NumberInput, TextInput, EmailInput, PasswordInput, Select
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import CustomUser, SEXE_CHOICES
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'tel', 'sexe', 'username', 'password1', 'password2']
        labels = {
            'email': _("Adresse Mail"),
            'first_name': _("Nom(s)"),
            'last_name': _("Prénom(s)"),
            'tel': _("Téléphone"),
            'sexe': _("Genre"),
            'username': _("Pseudo"),
            'password1': _("Mot de passe"),
            'password2': _("Confirmation du mot de passe"),
        }
        widgets = {
            'email': EmailInput(attrs={'class': 'tf-field-input tf-input'}),
            'first_name': TextInput(attrs={'class': 'tf-field-input tf-input', 'required': ''}),
            'last_name': TextInput(attrs={'class': 'tf-field-input tf-input'}),
            'tel': NumberInput(attrs={'class': 'tf-field-input tf-input', 'min': 0}),
            'sexe': Select(attrs={'class': 'tf-field-input tf-input'}),
            'username': TextInput(attrs={'class': 'tf-field-input tf-input'}),
            'password1': PasswordInput(attrs={'class': 'tf-field-input tf-input'}),
            'password2': PasswordInput(attrs={'class': 'tf-field-input tf-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('first_name'),
                Column('last_name'),
            ),
            PrependedText('email', '@', placeholder="email"),
        )


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=255, 
        widget=forms.EmailInput(attrs={
            'class': 'tf-field-input tf-input', 
            'placeholder': 'Adresse email', 
            'id': 'email', 
            'name': 'email'    
        }),
        label='Adresse email',
        required=True
    )
    password = forms.CharField(
        max_length=100, 
        widget=forms.PasswordInput(attrs={
            'class': 'tf-field-input tf-input',
            'placeholder': 'Mot de passe',
            'id': 'password',
            'name': 'password'
        }),
        label='Mot de passe',
        required=True
    )


class ProfileForm(UserChangeForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'tf-field-input tf-input',
            'placeholder': 'Adresse email',
            'id': 'email',
            'name': 'email',
            'autocomplete': 'off',
        }),
        label='Adresse email',
        required=True,
        disabled=True
    )
    
    tel = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'tf-field-input tf-input',
            'placeholder': 'Numéro de téléphone',
            'id': 'tel',
            'name': 'tel',
            'pattern': '[0-9]{8,1}',
            'minlength': '8',
            'maxlength': '15',
            'inputmode': 'numeric',
            'autocomplete': 'off',
        }),
        label="Numéro de téléphone",
        help_text="Veuillez entrer un numéro de téléphone valide (8 à 15 chiffres).",
        required=False
    )

    sexe = forms.ChoiceField(
        choices=[('', 'Sélectionner votre sexe')] + list(SEXE_CHOICES),
        widget=forms.Select(attrs={
            'class': 'tf-field-input tf-input',
            'id': 'sexe',
            'name': 'sexe'
        }),
        label="Sexe",
        required=False
    )

    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'tf-field-input tf-input',
            'placeholder': 'Mot de passe actuel',
            'id': 'current_password',
            'name': 'current_password',
            'autocomplete': 'new-password',
        }),
        label="Mot de passe actuel",
        required=False
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'tf-field-input tf-input',
            'placeholder': 'Nouveau mot de passe',
            'id': 'new_password',
            'name': 'new_password',
            'autocomplete': 'new-password',
        }),
        label="Nouveau mot de passe",
        help_text="Le mot de passe doit contenir au moins 8 caractères.",
        required=False
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'tf-field-input tf-input',
            'placeholder': 'Confirmer le nouveau mot de passe',
            'id': 'confirm_password',
            'name': 'confirm_password',
            'autocomplete': 'new-password',
        }),
        label="Confirmer le nouveau mot de passe",
        required=False
    )

    def clean_tel(self):
        tel = self.cleaned_data.get('tel')
        
        # Si le champ est vide, retourner None (car il est facultatif)
        if not tel:
            return None
        
        # Supprimer les espaces et les caractères spéciaux
        tel = ''.join(filter(str.isdigit, tel))  # Ne garder que les chiffres
        
        # Vérifier la longueur du numéro de téléphone (optionnel)
        if len(tel) < 8 or len(tel) > 15:
            raise forms.ValidationError("Le numéro de téléphone doit contenir entre 8 et 15 chiffres.")
        
        return tel

    def clean(self):
        cleaned_data = super().clean()
        tel = cleaned_data.get('tel')   
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        # Vérifier si l'utilisateur a fourni un mot de passe actuel
        if new_password or confirm_password:
            if not current_password:
                raise forms.ValidationError("Veuillez fournir votre mot de passe actuel pour modifier votre mot de passe.")

            # Vérifier si le mot de passe actuel est correct
            user = self.instance
            if not user.check_password(current_password):
                raise forms.ValidationError("Le mot de passe actuel est incorrect.")

            # Vérifier si les nouveaux mots de passe correspondent
            if new_password != confirm_password:
                raise forms.ValidationError("Les nouveaux mots de passe ne correspondent pas.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Supprimer le champ "password" du formulaire
        if 'password' in self.fields:
            del self.fields['password']

    class Meta:
        model = CustomUser
        fields = ['email', 'tel', 'sexe', 'current_password', 'new_password', 'confirm_password']
        exclude = ['password']

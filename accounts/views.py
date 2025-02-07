from django.contrib.auth import get_user_model, login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.forms import SignupForm, LoginForm, ProfileForm
from accounts.models import CustomUser

User = get_user_model()


def signup(request):
    """
    Gère l'inscription d'un nouvel utilisateur.

    Cette vue permet à un utilisateur de créer un compte en remplissant un formulaire d'inscription.
    Si la requête est de type POST et que les données du formulaire sont valides :
    - Un nouvel utilisateur est créé et enregistré en base de données.
    - Un objet `CustomUser` est associé à cet utilisateur.
    - L'utilisateur est automatiquement connecté après son inscription.
    - Il est ensuite redirigé vers la page d'accueil (`index`).

    Si la requête est de type GET, un formulaire vide est affiché.

    Args:
        request (HttpRequest): L'objet requête HTTP contenant les données de l'utilisateur.

    Returns:
        HttpResponse: La page d'inscription (`accounts/signup.html`), contenant le formulaire d'inscription.
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("Nom du nouvel utilisateur : " + user.username)
            CustomUser.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html", locals())


def login_user(request):
    message = ''
    page_title = "Connexion"
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
        if user is not None:
            login(request, user)
            message = f'Bonjour {user.email}, vous êtes connecté.'
            return redirect("home")
        else:
            message = "Nom d'utilisateur ou mot de passe incorrect."
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", locals())


def logout_user(request):
    logout(request)
    return redirect('home')


@login_required
def profil(request):
    message = ''
    page_title = "Mon Compte"
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            # Mettre à jour la session pour éviter de déconnecter l'utilisateur
            update_session_auth_hash(request, user)
            messages.success(request, "Votre profil a été mis à jour avec succès !")
            return redirect('accounts:profil')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'accounts/profil.html', {
        'form': form,
        'page_title': page_title,
        'message': message
    })

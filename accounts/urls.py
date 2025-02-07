from django.urls import path
from accounts.views import *
from django.views.generic import TemplateView


app_name = 'accounts'
urlpatterns = [
    path('profil/', profil, name='profil'),
    path('signup/', signup, name="signup"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
]

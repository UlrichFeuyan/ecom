from django.contrib.auth.models import AbstractUser
from django.db import models

SEXE_CHOICES = [
    ('masculin', 'Masculin'),
    ('feminin', 'Féminin'),
]


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=False)
    tel = models.IntegerField(null=True)
    sexe = models.CharField(max_length=15, choices=SEXE_CHOICES, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

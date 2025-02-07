from django.db import models
from core.settings import AUTH_USER_MODEL


class Customer(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.user.username

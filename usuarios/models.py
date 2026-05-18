from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    class Perfil(models.TextChoices):
        ADMINISTRADOR = 'ADM', 'Administrador'
        PERITO        = 'PER', 'Perito'
        SOLICITANTE   = 'SOL', 'Solicitante'

    email = models.EmailField(unique=True)
    perfil = models.CharField(
        max_length=3,
        choices=Perfil.choices,
        default=Perfil.SOLICITANTE,
    )

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.email} ({self.get_perfil_display()})'
from django.conf import settings
from django.db import models

from protocolos.models import Protocolo


class Laudo(models.Model):
    protocolo   = models.OneToOneField(
        Protocolo,
        on_delete=models.PROTECT,
        related_name='laudo',
    )
    perito      = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='laudos_gerados',
    )
    conteudo    = models.TextField()         
    arquivo     = models.FileField(        
        upload_to='laudos/',
        null=True,
        blank=True,
    )
    gerado_em   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Laudo do Protocolo #{self.protocolo_id}'
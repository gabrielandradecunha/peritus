from django.conf import settings
from django.db import models


class Protocolo(models.Model):
    class Status(models.TextChoices):
        ABERTO     = 'ABT', 'Aberto'
        EM_TRAMITE = 'TRM', 'Em Trâmite'
        FINALIZADO = 'FIN', 'Finalizado'
    
    class Prioridade(models.TextChoices):
        NORMAL       = 'NOR', 'Normal'
        URGENTE      = 'URG', 'Urgente'
        MUITO_URGENTE = 'MUR', 'Muito Urgente'

    prioridade = models.CharField(
        max_length=3,
        choices=Prioridade.choices,
        default=Prioridade.NORMAL,
    )
    obs = models.TextField(blank=True, default='')

    titulo      = models.CharField(max_length=200)
    descricao   = models.TextField()
    status      = models.CharField(
        max_length=3,
        choices=Status.choices,
        default=Status.EM_TRAMITE,
    )
    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='protocolos_solicitados',
    )
    perito = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='protocolos_atribuidos',
    )
    criado_em   = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Protocolo #{self.pk} – {self.titulo} [{self.get_status_display()}]'
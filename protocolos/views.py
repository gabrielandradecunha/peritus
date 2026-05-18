from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Protocolo
from usuarios.models import Usuario

@login_required
def protocolos_view(request):
    context = {
        'protocolos': Protocolo.objects.select_related('solicitante', 'perito').order_by('-criado_em'),
        'peritos': Usuario.objects.filter(perfil='PER'),
    }
    return render(request, 'protocolos.html', context)


@login_required
def protocolo_novo_view(request):
    peritos = Usuario.objects.filter(perfil='PER')
    if request.method == 'POST':
        titulo    = request.POST.get('titulo', '').strip()
        descricao = request.POST.get('descricao', '').strip()
        prioridade = request.POST.get('prioridade', 'NOR')
        perito_id  = request.POST.get('perito_id')
        obs        = request.POST.get('obs', '')

        if not titulo or not descricao or not prioridade:
            return render(request, 'protocolo-novo.html', {
                'erro': 'Preencha todos os campos obrigatórios.',
                'peritos': peritos,
            })

        perito = None
        status = 'ABT'
        if perito_id:
            perito = get_object_or_404(Usuario, pk=perito_id)
            status = 'TRM'

        Protocolo.objects.create(
            titulo=titulo,
            descricao=descricao,
            prioridade=prioridade,
            solicitante=request.user,
            perito=perito,
            status=status,
            obs=obs,
        )
        return redirect('protocolos')

    return render(request, 'protocolo-novo.html', {'peritos': peritos})


@login_required
def atribuir_perito_view(request):
    if request.method == 'POST':
        protocolo = get_object_or_404(Protocolo, pk=request.POST['protocolo_id'])
        perito    = get_object_or_404(Usuario,   pk=request.POST['perito_id'])
        protocolo.perito = perito
        protocolo.status = 'TRM'
        protocolo.save()
    return redirect('protocolos')


@login_required
def finalizar_protocolo_view(request):
    if request.method == 'POST':
        protocolo = get_object_or_404(Protocolo, pk=request.POST['protocolo_id'])
        protocolo.status = 'FIN'
        protocolo.save()
    return redirect('protocolos')
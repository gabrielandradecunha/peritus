from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from documentos.models import Laudo
from protocolos.models import Protocolo


@login_required
def documentos_view(request):
    context = {
        'laudos': Laudo.objects.select_related('protocolo', 'perito').order_by('-gerado_em'),
        'protocolos_disponiveis': Protocolo.objects.filter(
            status='TRM', laudo__isnull=True
        ).select_related('perito'),
        'hoje': timezone.now().date().isoformat(),
    }
    return render(request, 'documentos.html', context)


@login_required
def gerar_laudo_view(request):
    if request.method == 'POST':
        protocolo_id = request.POST.get('protocolo_id')
        objetivo     = request.POST.get('objetivo', '').strip()
        metodologia  = request.POST.get('metodologia', '').strip()
        analise      = request.POST.get('analise', '').strip()
        conclusao    = request.POST.get('conclusao', '').strip()

        if not all([protocolo_id, objetivo, metodologia, analise, conclusao]):
            laudos = Laudo.objects.select_related('protocolo', 'perito').order_by('-gerado_em')
            protocolos = Protocolo.objects.filter(status='TRM', laudo__isnull=True)
            return render(request, 'documentos.html', {
                'laudos': laudos,
                'protocolos_disponiveis': protocolos,
                'hoje': timezone.now().date().isoformat(),
                'erro': 'Preencha todos os campos obrigatórios.',
                'tab_ativa': 'gerar',
            })

        protocolo = get_object_or_404(Protocolo, pk=protocolo_id)
        conteudo = f"1. OBJETIVO\n{objetivo}\n\n2. METODOLOGIA\n{metodologia}\n\n3. ANÁLISE E RESULTADOS\n{analise}\n\n4. CONCLUSÃO\n{conclusao}"

        Laudo.objects.create(
            protocolo=protocolo,
            perito=request.user,
            conteudo=conteudo,
        )
        protocolo.status = 'FIN'
        protocolo.save()

        return render(request, 'documentos.html', {
            'laudos': Laudo.objects.select_related('protocolo', 'perito').order_by('-gerado_em'),
            'protocolos_disponiveis': Protocolo.objects.filter(status='TRM', laudo__isnull=True),
            'hoje': timezone.now().date().isoformat(),
            'sucesso': 'Laudo gerado com sucesso e protocolo finalizado.',
        })

    return redirect('documentos')
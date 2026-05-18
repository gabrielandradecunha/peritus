from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Usuario


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email    = request.POST['email']
        password = request.POST['password']
        usuario  = authenticate(request, email=email, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('home')
        return render(request, 'login.html', {'erro': 'E-mail ou senha incorretos.'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home_view(request):
    from protocolos.models import Protocolo
    context = {
        'total_abertos':     Protocolo.objects.filter(status='ABT').count(),
        'total_tramite':     Protocolo.objects.filter(status='TRM').count(),
        'total_finalizados': Protocolo.objects.filter(status='FIN').count(),
        'total_usuarios':    Usuario.objects.filter(is_active=True).count(),
        'protocolos_recentes': Protocolo.objects.select_related('solicitante', 'perito').order_by('-criado_em')[:5],
    }
    return render(request, 'home.html', context)


def _somente_admin(request):
    return request.user.is_authenticated and request.user.perfil == 'ADM'


@login_required
def usuarios_view(request):
    context = {
        'usuarios': Usuario.objects.order_by('first_name', 'email'),
        'is_admin': _somente_admin(request),
    }
    return render(request, 'usuarios.html', context)


@login_required
def criar_usuario_view(request):
    if not _somente_admin(request):
        return redirect('usuarios')
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        email      = request.POST.get('email', '').strip()
        perfil     = request.POST.get('perfil', '')
        senha      = request.POST.get('senha', '')
        confirmar  = request.POST.get('confirmar_senha', '')

        def _renderizar_erro(msg):
            return render(request, 'usuarios.html', {
                'usuarios': Usuario.objects.order_by('first_name', 'email'),
                'is_admin': True,
                'erro': msg,
            })

        if senha != confirmar:
            return _renderizar_erro('As senhas não coincidem.')
        if len(senha) < 8:
            return _renderizar_erro('A senha deve ter no mínimo 8 caracteres.')
        if Usuario.objects.filter(email=email).exists():
            return _renderizar_erro('Já existe um usuário com este e-mail.')

        u = Usuario.objects.create_user(
            username=email,
            email=email,
            password=senha,
            first_name=first_name,
            last_name=last_name,
            perfil=perfil,
        )
        return render(request, 'usuarios.html', {
            'usuarios': Usuario.objects.order_by('first_name', 'email'),
            'is_admin': True,
            'sucesso': f'Usuário {u.get_full_name()} cadastrado com sucesso.',
        })
    return redirect('usuarios')


@login_required
def editar_usuario_view(request, pk):
    if not _somente_admin(request):
        return redirect('usuarios')
    u = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        u.first_name = request.POST.get('first_name', '').strip()
        u.last_name  = request.POST.get('last_name', '').strip()
        u.email      = request.POST.get('email', '').strip()
        u.username   = u.email
        u.perfil     = request.POST.get('perfil', u.perfil)
        u.save()
        return render(request, 'usuarios.html', {
            'usuarios': Usuario.objects.order_by('first_name', 'email'),
            'is_admin': True,
            'sucesso': f'Usuário {u.get_full_name()} atualizado com sucesso.',
        })
    return redirect('usuarios')


@login_required
def toggle_usuario_view(request, pk):
    if not _somente_admin(request):
        return redirect('usuarios')
    if request.method == 'POST':
        u = get_object_or_404(Usuario, pk=pk)
        if u.pk != request.user.pk:
            u.is_active = not u.is_active
            u.save()
    return redirect('usuarios')


@login_required
def perfil_view(request):
    from protocolos.models import Protocolo
    from documentos.models import Laudo
    context = {
        'total_protocolos':    Protocolo.objects.filter(solicitante=request.user).count(),
        'total_laudos':        Laudo.objects.filter(perito=request.user).count(),
        'total_usuarios':      Usuario.objects.count(),
        'protocolos_recentes': Protocolo.objects.filter(
            solicitante=request.user).order_by('-criado_em')[:3],
        'laudos_recentes':     Laudo.objects.filter(
            perito=request.user).order_by('-gerado_em')[:3],
    }
    return render(request, 'perfil.html', context)


@login_required
def editar_perfil_view(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '').strip()
        request.user.last_name  = request.POST.get('last_name', '').strip()
        request.user.email      = request.POST.get('email', '').strip()
        request.user.username   = request.user.email
        request.user.save()
        return render(request, 'perfil.html', {'sucesso': 'Perfil atualizado com sucesso.'})
    return redirect('perfil')


@login_required
def alterar_senha_view(request):
    if request.method == 'POST':
        from django.contrib.auth import update_session_auth_hash
        senha_atual = request.POST.get('senha_atual', '')
        nova_senha  = request.POST.get('nova_senha', '')
        confirmar   = request.POST.get('confirmar_senha', '')

        if not request.user.check_password(senha_atual):
            return render(request, 'perfil.html', {'erro': 'Senha atual incorreta.'})
        if nova_senha != confirmar:
            return render(request, 'perfil.html', {'erro': 'As senhas não coincidem.'})
        if len(nova_senha) < 8:
            return render(request, 'perfil.html', {'erro': 'A nova senha deve ter no mínimo 8 caracteres.'})

        request.user.set_password(nova_senha)
        request.user.save()
        update_session_auth_hash(request, request.user)
        return render(request, 'perfil.html', {'sucesso': 'Senha alterada com sucesso.'})
    return redirect('perfil')
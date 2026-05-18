from django.contrib import admin
from django.urls import path
from usuarios import views as u
from protocolos import views as p
from documentos import views as d

urlpatterns = [
    path('admin/',                      admin.site.urls),
    path('',                            u.login_view,           name='login'),
    path('logout/',                     u.logout_view,          name='logout'),
    path('home/',                       u.home_view,            name='home'),
    path('usuarios/',                   u.usuarios_view,        name='usuarios'),
    path('usuarios/criar/',             u.criar_usuario_view,   name='criarUsuario'),
    path('usuarios/<int:pk>/editar/',   u.editar_usuario_view,  name='editarUsuario'),
    path('usuarios/<int:pk>/toggle/',   u.toggle_usuario_view,  name='toggleUsuario'),
    path('perfil/',                     u.perfil_view,          name='perfil'),
    path('perfil/editar/', u.editar_perfil_view, name='editarPerfil'),
    path('perfil/senha/',  u.alterar_senha_view, name='alterarSenha'),    
    path('protocolos/',                 p.protocolos_view,      name='protocolos'),
    path('protocolos/novo/',            p.protocolo_novo_view,  name='protocolo_novo'),
    path('protocolos/atribuir/',        p.atribuir_perito_view, name='atribuir_perito'),
    path('protocolos/finalizar/',       p.finalizar_protocolo_view, name='finalizar_protocolo'),
    path('documentos/',                 d.documentos_view,      name='documentos'),
    path('documentos/gerar/',           d.gerar_laudo_view,     name='gerar_laudo'),
]
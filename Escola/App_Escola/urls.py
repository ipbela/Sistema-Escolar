from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.abre_index, name='abre_index'),
    path('cadastro', views.abre_cadastro_professor, name='abre_cadastro'),
    path('enviar_login', views.enviar_login, name='enviar_login'),
    path('confirmar_cadastro', views.confirmar_cadastro, name='confirmar_cadastro'),

    path('cad_turma/<int:id_professor>', views.cad_turma, name='cad_turma'),
    path('salvar_turma_nova', views.salvar_turma_nova, name='salvar_turma_nova'),

    path('home/<int:id_professor>/<int:id_logado>', views.home, name='home'),

    path('excluir_turma/<int:id_turma>/', views.excluir_turma, name='excluir_turma'),
    path('ver_turma/<int:id_turma>/<int:id_professor>/', views.ver_turma, name='ver_turma'),
    path('confAcao/<int:id_turma>/', views.confAcao, name='confAcao'),

    path('cad_atividade/<int:id_professor>/', views.cad_atividade, name='cad_atividade'),
    path('salvar_atividade_nova', views.salvar_atividade_nova, name='salvar_atividade_nova'),
    path('excluir_atividade/<int:id_turma>/<int:id_atividade>/', views.excluir_atividade, name='excluir_atividade'),
    path('ver_atividade/<int:id_professor>/<int:id_atividade>/', views.ver_atividade, name='ver_atividade'),
    path('confAtiv/<int:id_turma>/<int:id_atividade>/', views.confAtiv, name='confAtiv'),

    path('fazer_logout/', views.fazer_logout, name='fazer_logout'),

]

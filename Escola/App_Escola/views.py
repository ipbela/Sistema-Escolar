from django.shortcuts import render, redirect, get_object_or_404
from hashlib import sha256
from .models import Professor, Turma, Atividade
from django.db import connection, transaction
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import logout

def abre_index(request):
    return render(request, 'login.html')

def abre_cadastro_professor(request):
    return render(request, '/cadastro.html')

def enviar_login(request):
    if(request.method == 'POST'):
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha_criptografada = sha256(senha.encode()).hexdigest()
        dados_professor = Professor.objects.filter(email=email).values("nome", "senha", "id")

        if dados_professor:
            senha = dados_professor[0]
            senha = senha['senha']
            usuario_logado = dados_professor[0]
            usuario_logado = usuario_logado['nome']
            if(senha == senha_criptografada):
                id_logado = dados_professor[0]
                id_logado = id_logado['id']
                turmas_do_professor = Turma.objects.filter(id_professor = id_logado)

                atividades_todas_turmas = []
                for turma in turmas_do_professor:
                    atividades = Atividade.objects.filter(id_turma=turma.id)
                    atividades_todas_turmas.extend(atividades)

                return render(request, 'home.html', {'nome': email, 'turmas_do_professor': turmas_do_professor, 'id_logado': id_logado, 'usuario_logado': usuario_logado, 'atividades_todas_turmas': atividades_todas_turmas})
            
            else:
                messages.error(request, 'Usuário ou senha incorretos. Tente novamente.')
                return render(request, 'login.html', {'email': email})
        
        return render(request, 'cadastro.html', {'login': email})
    else:
        return render(request, 'login.html')

def confirmar_cadastro(request):
    if(request.method == 'POST'):
        nome = request.POST.get('nome')
        email = request.POST.get('login')
        senha = request.POST.get('senha')
        senha_criptografada = sha256(senha.encode()).hexdigest()

        grava_professor = Professor(
            nome=nome,
            email=email,
            senha=senha_criptografada
        )
        grava_professor.save()

        return render(request, 'login.html', {'email': email})
    
def cad_turma(request, id_professor):
    usuario_logado = Professor.objects.filter(id=id_professor).values("nome", "id")
    usuario_logado = usuario_logado[0]
    usuario_logado = usuario_logado['nome']

    return render(request, "cad_turma.html", {'usuario_logado':usuario_logado, 'id_logado':id_professor})

def home(request, id_professor, id_logado):
    dados_professor = Professor.objects.filter(id=id_professor).values("nome", "id")
    usuario_logado = dados_professor[0]
    usuario_logado = usuario_logado['nome']
    id_logado = dados_professor[0]
    id_logado = id_logado['id']
    turmas_do_professor = Turma.objects.filter(id_professor = id_logado)

    atividades_todas_turmas = []
    for turma in turmas_do_professor:
        atividades = Atividade.objects.filter(id_turma=turma.id)
        atividades_todas_turmas.extend(atividades)

    return render(request, 'home.html', {
        'id_professor': id_professor,
        'id_logado': id_logado,
        'turmas_do_professor': turmas_do_professor,
        'usuario_logado': usuario_logado,
        'atividades_todas_turmas': atividades_todas_turmas,
    })


def salvar_turma_nova(request):
    if(request.method == 'POST'):
        nome_turma = request.POST.get('nome_turma')
        id_professor = request.POST.get('id_professor')

        professor = Professor.objects.get(id=id_professor)
        turma_existente = Turma.objects.filter(nome_turma=nome_turma, id_professor=professor).exists()

        dados_professor = Professor.objects.filter(id=id_professor).values("nome", "id")
        usuario_logado = dados_professor[0]['nome']
        id_logado = dados_professor[0]['id']

        if turma_existente:
            messages.error(request, 'Essa turma já existe!')
            return render(request, "cad_turma.html", {'usuario_logado':usuario_logado, 'id_logado':id_professor})
        else:
            grava_turma = Turma(
                nome_turma = nome_turma,
                id_professor = professor
            )

            grava_turma.save()
            # messages.info(request, "Turma cadastrada com sucesso.")

            dados_professor = Professor.objects.filter(id=id_professor).values("nome", "id")
            usuario_logado = dados_professor[0]
            usuario_logado = usuario_logado['nome']
            id_logado = dados_professor[0]
            id_logado = id_logado['id']

            return redirect('home', id_professor=id_professor, id_logado=id_logado)
    

def ver_turma(request, id_turma, id_professor):
    turma = get_object_or_404(Turma, id=id_turma)
    professor = get_object_or_404(Professor, id=id_professor)

    dados_professor = Professor.objects.filter(id=id_professor).values("nome", "id")
    usuario_logado = dados_professor[0]['nome']
    id_logado = dados_professor[0]['id']
    turmas_do_professor = Turma.objects.filter(id_professor=id_logado)

    atividades_turma = Atividade.objects.filter(id_turma=turma)

    return render(request, 'turma.html', {'turma': turma, 'usuario_logado': usuario_logado, 'turmas_do_professor': turmas_do_professor, 'id_logado': id_logado, 'atividades_turma': atividades_turma})
    

def confAcao(request, id_turma):
    return render(request, 'confAcao.html', {'id_turma': id_turma})

def excluir_turma(request, id_turma):
    if (request.method == 'POST'):
        turma = get_object_or_404(Turma, id=id_turma)
        atividades = Atividade.objects.filter(id_turma=turma)
        atividades.delete()  
        id_professor = turma.id_professor.id
        turma.delete()
        return redirect('home', id_professor=id_professor, id_logado=id_professor)
    else:
        return HttpResponse(status=405)  


def cad_atividade(request, id_professor):
    usuario_logado = Professor.objects.filter(id=id_professor).values("nome", "id")
    usuario_logado = usuario_logado[0]
    usuario_logado = usuario_logado['nome']
    
    return render(request, "cad_atividade.html", {'usuario_logado': usuario_logado, 'id_logado': id_professor})


def salvar_atividade_nova(request):
    if (request.method == 'POST'):
        nome_atividade = request.POST.get('nome_atividade')
        id_professor = request.POST.get('id_professor')
        id_turma = request.POST.get('id_turma')  

        dados_professor = Professor.objects.filter(id=id_professor).values("nome", "id")
        usuario_logado = dados_professor[0]
        usuario_logado = usuario_logado['nome']
        id_logado = dados_professor[0]
        id_logado = id_logado['id']

        try:
            turma = Turma.objects.get(id=id_turma)
        except Turma.DoesNotExist:
            messages.error(request, 'Essa turma não existe. Verifique o código da turma e tente novamente.')
            return render(request, 'cad_atividade.html', {'nome_atividade': nome_atividade, 'id_logado': id_professor})

        grava_atividade = Atividade(
            nome_atividade=nome_atividade,
            id_turma=turma
        )
        grava_atividade.save()

        return redirect('home', id_professor=id_professor, id_logado=id_logado)

    return HttpResponse(status=405)


def ver_atividade(request, id_professor, id_atividade):
    
    atividade = get_object_or_404(Atividade, id=id_atividade)
    
    professor = get_object_or_404(Professor, id=id_professor)

    dados_professor = Professor.objects.filter(id=id_professor).values("nome", "id")
    usuario_logado = dados_professor[0]['nome']
    id_logado = dados_professor[0]['id']
    turmas_do_professor = Turma.objects.filter(id_professor=id_logado)

    return render(request, 'atividade.html', {
        'atividade': atividade,
        'professor': professor,
        'usuario_logado': usuario_logado,
        'turmas_do_professor': turmas_do_professor,
        'id_logado': id_logado
    })
    

def confAtiv(request, id_turma, id_atividade):
    return render(request, 'confAtiv.html', {'id_turma': id_turma, 'id_atividade': id_atividade})

    
def excluir_atividade(request, id_turma, id_atividade):
    if (request.method == 'POST'):
        atividade = get_object_or_404(Atividade, id=id_atividade)
        turma = get_object_or_404(Turma, id=id_turma)
        id_professor = turma.id_professor.id
        atividade.delete()
        professor = get_object_or_404(Professor, id=id_professor)
        id_logado = professor.id
        return redirect('home', id_professor=id_professor, id_logado=id_logado)
    else:
        return HttpResponse(status=405)

def fazer_logout(request):
    logout(request)
    #redireciona para a primeira pagina
    return render(request, 'Login.html')
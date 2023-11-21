from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Cadastro de usuarios

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As Senhas não Conferem')
            return redirect('/usuarios/cadastro')
        if len(senha) < 6:
            messages.add_message(request, constants.WARNING, 'Sua senha é menor que 7 digitos')
            return redirect('/usuarios/cadastro')
        try:
            # Username deve ser único!
            user = User.objects.create_user(
            first_name=primeiro_nome,
            last_name=ultimo_nome,
            username=username,
            email=email,
            password=senha,
        )
            messages.add_message(request, constants.SUCCESS, 'Usuario Cadastrado com Sucesso')
        except:
             messages.add_message(request, constants.ERROR, 'Algo não ocorreu certo. Contate o suporte.')
             return redirect('/usuarios/cadastro')
        
        
        return redirect('/usuarios/login')

# Login

def logar(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method =="POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        user = authenticate(username=username, password=senha)
    if user:
        login(request, user)

        if user.is_staff:
            return redirect('/empresarial/gerenciar_clientes')
        elif not user.is_staff:
            return redirect('/exame/solicitar_exames')

    else:
        messages.add_message(request, constants.ERROR, 'Usuario ou senha inválidos')
        return redirect('/usuarios/login')
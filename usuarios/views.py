from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from .decorators import manager_required


@login_required
@manager_required
def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(username=username).first()
        if user:
            return HttpResponse('Usuário já cadastrado!')
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return HttpResponse('Cadastrado com Sucesso!')

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user :
            login_django(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
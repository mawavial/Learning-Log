from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm

def logout_view(request):
    """Faz logout do usuario"""
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))

def register(request):
    """Faz o cadastro de um novo usuario"""
    if request.method != 'POST':
        #Exibe o formulario de cadastro em branco
        form = UserCreationForm()
    else:
        #Processa o formulario
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            #Faz login do usuario o redireciona para a pagina inicial
            authenticate_user = authenticate(username=new_user.username, password=request.POST['password'])
            login(request, authenticate_user)
            return HttpResponseRedirect(reverse('learning_logs:index'))
    context = {'form': form}
    return render(request,'users/register.html', context)

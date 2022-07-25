from hashlib import new
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm

def logout_view(request):
    '''Завершает сеанс работы с приложением'''
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    '''Регистрирует нового пользователя'''
    if request.method !=  'POST':
        # Отображает форму регистрации
        form = UserCreationForm()
    else:
        # Обработка заполненной формы
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # Выполнение входа и перенапраыление на домашнюю страицу
            authenticated_user = authenticate(username=new_user.username,
                password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('index'))
    context = {'form': form}
    return render(request, 'users/register.html', context)

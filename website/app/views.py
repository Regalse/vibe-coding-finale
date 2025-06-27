from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    return render(request, 'index.html')

def legal(request):
    return render(request, 'legal.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        new_username = request.POST.get('username', '').strip()
        if new_username and new_username != user.username:
            if not User.objects.filter(username=new_username).exists():
                user.username = new_username
                user.save()
                messages.success(request, 'Имя пользователя успешно изменено!')
            else:
                messages.error(request, 'Пользователь с таким именем уже существует.')
        else:
            messages.error(request, 'Новое имя пользователя должно отличаться от текущего.')
    return render(request, 'profile.html', {'user': user})

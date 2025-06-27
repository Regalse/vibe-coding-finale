from django.shortcuts import render, get_object_or_404
from .forms import CustomUserCreationForm, PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Post
from django.http import HttpResponseForbidden

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
    user_posts = user.posts.all().order_by('-created_at')
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
    return render(request, 'profile.html', {'user': user, 'user_posts': user_posts})

def threads(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'threads.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Пост успешно опубликован!')
            return redirect('threads')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.select_related('author').order_by('created_at')
    form = None
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
                messages.success(request, 'Комментарий добавлен!')
                return redirect('post_detail', post_id=post.id)
        else:
            form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return HttpResponseForbidden('Вы не можете удалить этот пост.')
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Пост успешно удалён!')
        return redirect('profile')
    return redirect('profile')

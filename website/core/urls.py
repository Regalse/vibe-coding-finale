"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import index, legal, register, login_view, profile, threads, create_post, post_detail, delete_post

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('legal/', legal, name='legal'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('profile/', profile, name='profile'),
    path('threads/', threads, name='threads'),
    path('threads/create/', create_post, name='create_post'),
    path('threads/<int:post_id>/', post_detail, name='post_detail'),
    path('threads/<int:post_id>/delete/', delete_post, name='delete_post'),
]

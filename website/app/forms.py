from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    agree = forms.BooleanField(
        required=True,
        label='Я соглашаюсь с <a href="/legal/" target="_blank">пользовательским соглашением</a>',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "agree")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['agree'].label = ''

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название поста'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите текст поста', 'rows': 6}),
        }
        labels = {
            'title': 'Название',
            'body': 'Тело поста',
        } 
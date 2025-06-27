from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
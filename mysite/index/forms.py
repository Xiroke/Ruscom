from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignInForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Введите электронную почту', }), label='Почта')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль', }), label='Пароль')
    


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SearchArticleForm(forms.ModelForm):
    search = forms.CharField(max_length=100)
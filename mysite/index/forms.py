from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignInForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Введите электронную почту', }), label='Почта')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль', }), label='Пароль')
    


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'placeholder': 'Введите логин', }), label='Логин')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Введите электронную почту', }), label='Почта')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль', }), label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль ещё раз', }), label='Пароль ещё раз')
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SearchArticleForm(forms.ModelForm):
    search = forms.CharField(max_length=100)
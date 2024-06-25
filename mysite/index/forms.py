from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from .models import TaskSimpleModel, DictionaryModel


class LoginForm(AuthenticationForm):
  #username is email
  username = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Введите электронную почту', }), label='Почта')
  password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль', }), label='Пароль')
  
  class Meta:
    model = get_user_model()
    fields = ['username', 'password']

class RegisterForm(UserCreationForm):
  name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Введите имя', }), label='Имя')
  email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Введите электронную почту', }), label='Почта')
  password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль', }), label='Пароль')
  password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль ещё раз', }), label='Пароль ещё раз')
  class Meta:
    model = get_user_model()
    fields = ['name', 'email', 'password1', 'password2']


class TaskSimpleForm(forms.ModelForm):
  answer = forms.CharField(label = '', widget=forms.TextInput(attrs={'autocomplete': 'off'}))

  class Meta:
    model = TaskSimpleModel
    fields = ['answer']


class SearchTestsForm(forms.ModelForm):
  title = forms.CharField(label = '')

  class Meta:
    model = TaskSimpleModel
    fields = ['title']


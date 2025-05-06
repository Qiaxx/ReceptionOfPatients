from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from users.models import User


class LoginForm(forms.Form):
    email = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'px-4 pt-5 pb-2 w-full h-12 rounded border border-teal-600 border-solid duration-[0.25s] transition-[border-color]',
            'id': 'email-input',
        }),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'px-4 pt-5 pb-2 w-full h-12 rounded border border-solid border-zinc-200 duration-[0.25s] transition-[border-color]',
            'id': 'password-input',
        }),
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise forms.ValidationError("Неверный логин или пароль")

        return cleaned_data


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'px-4 pt-5 pb-2 w-full h-12 rounded border border-solid border-zinc-200 duration-[0.25s] transition-[border-color]',
            'id': 'email-input',
        }),
    )
    phone = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'px-4 pt-5 pb-2 w-full h-12 rounded border border-solid border-zinc-200 duration-[0.25s] transition-[border-color]',
            'id': 'phone-input',
        }),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'px-4 pt-5 pb-2 w-full h-12 rounded border border-solid border-zinc-200 duration-[0.25s] transition-[border-color]',
            'id': 'password-input',
        }),
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password
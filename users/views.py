from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages

from users.forms import UserRegistrationForm, LoginForm
from users.models import User


class LoginView(View):
    template_name = 'users/login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('system:choose')
            else:
                messages.error(request, 'Неверный логин или пароль')
        return render(request, self.template_name, {'form': form})

class RegisterView(View):
    model = User
    template_name = 'users/register.html'
    success_url = reverse_lazy("system_profile:register_patient_profile")

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print("✅ Форма валидна")
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']

            user = User.objects.create_user(
                email=email,
                password=password
            )
            user.phone = phone
            user.save()

            login(request, user)
            messages.success(request, 'Регистрация успешно завершена!')
            return redirect(self.success_url)
        else:
            print("❌ Ошибки формы:", form.errors)

        return render(request, self.template_name, {'form': form})



class ForgotPasswordView(View):
    template_name = 'users/forgot_password.html'

    def get(self, request):
        return render(request, self.template_name, {})

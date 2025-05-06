from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import LoginView
from users.apps import UsersConfig

from users.views import RegisterView, ForgotPasswordView

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page='patient/login/'), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
]
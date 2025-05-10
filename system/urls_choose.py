from django.urls import path

from system.apps import SystemConfig
from system.views import ChooseView

app_name = SystemConfig.name

urlpatterns = [
    path('choose/', ChooseView.as_view(), name='choose'),
]
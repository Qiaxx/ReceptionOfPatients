from django.urls import path

from system.apps import SystemConfig
from system.views import RegisterPatientProfileView

app_name = SystemConfig.name

urlpatterns = [
    path('', RegisterPatientProfileView.as_view(), name='register_patient_profile'),
]
from django.urls import path

from system import views
from system.apps import SystemConfig
from system.views import ChooseView, DoctorsView, AppointmentView

app_name = SystemConfig.name

urlpatterns = [
    path('choose/', ChooseView.as_view(), name='choose'),
    path('<int:pk>/doctors/', DoctorsView.as_view(), name='doctors'),
    path('appointment/<int:doctor_id>/', AppointmentView.as_view(), name='appointment'),
    path('api/free_slots/', views.get_free_slots, name='get_free_slots'),
]
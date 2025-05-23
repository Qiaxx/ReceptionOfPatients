from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('patient/', include('users.urls', namespace='users')),
    path('patient/', include('system.urls', namespace='system')),
    path('patient/register/profile/', include('system.urls_profile', namespace='system_profile')),
    path('', RedirectView.as_view(url='/patient/login/')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
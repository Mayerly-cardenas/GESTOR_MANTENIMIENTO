from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('Inicio.urls')),
    path('admin/', admin.site.urls),
    path('cuentas/', include('Cuentas.urls')),
    path('motores/', include('Motores.urls')),
    path('mantenimiento-electrico/', include('Mantenimiento_Electrico.urls')),
    path('mantenimiento-mecanico/', include('Mantenimiento_Mecanico.urls')),
    path('mantenimiento-preventivo/', include('Mantenimiento_Preventivo.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path

from . import views

app_name = "mantenimiento_electrico"

urlpatterns = [
    path("", views.RegistroActividadListView.as_view(), name="index"),
    path("nuevo/", views.RegistroActividadCreateView.as_view(), name="registro_create"),
    path("<int:pk>/", views.RegistroActividadDetailView.as_view(), name="registro_detail"),
    path("<int:pk>/eliminar/", views.RegistroActividadDeleteView.as_view(), name="registro_delete"),
]

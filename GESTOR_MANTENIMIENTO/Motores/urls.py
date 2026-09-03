from django.urls import path

from . import views

app_name = "motores"

urlpatterns = [
    path("", views.MotorListView.as_view(), name="motor_list"),
    path("nuevo/", views.MotorCreateView.as_view(), name="motor_create"),
    path("<int:pk>/", views.MotorDetailView.as_view(), name="motor_detail"),
    path("<int:pk>/editar/", views.MotorUpdateView.as_view(), name="motor_update"),
    path("<int:pk>/eliminar/", views.MotorDeleteView.as_view(), name="motor_delete"),

    path("fabricas/", views.FabricaListView.as_view(), name="fabrica_list"),
    path("fabricas/nueva/", views.FabricaCreateView.as_view(), name="fabrica_create"),
    path("fabricas/<int:pk>/editar/", views.FabricaUpdateView.as_view(), name="fabrica_update"),
    path("fabricas/<int:pk>/eliminar/", views.FabricaDeleteView.as_view(), name="fabrica_delete"),

    path("fabricantes/", views.FabricanteListView.as_view(), name="fabricante_list"),
    path("fabricantes/nuevo/", views.FabricanteCreateView.as_view(), name="fabricante_create"),
    path("fabricantes/<int:pk>/editar/", views.FabricanteUpdateView.as_view(), name="fabricante_update"),
    path("fabricantes/<int:pk>/eliminar/", views.FabricanteDeleteView.as_view(), name="fabricante_delete"),

    path("ubicaciones/", views.UbicacionListView.as_view(), name="ubicacion_list"),
    path("ubicaciones/nueva/", views.UbicacionCreateView.as_view(), name="ubicacion_create"),
    path("ubicaciones/<int:pk>/editar/", views.UbicacionUpdateView.as_view(), name="ubicacion_update"),
    path("ubicaciones/<int:pk>/eliminar/", views.UbicacionDeleteView.as_view(), name="ubicacion_delete"),

    path("salas-electricas/", views.SalaElectricaListView.as_view(), name="sala_list"),
    path("salas-electricas/nueva/", views.SalaElectricaCreateView.as_view(), name="sala_create"),
    path("salas-electricas/<int:pk>/editar/", views.SalaElectricaUpdateView.as_view(), name="sala_update"),
    path("salas-electricas/<int:pk>/eliminar/", views.SalaElectricaDeleteView.as_view(), name="sala_delete"),
]

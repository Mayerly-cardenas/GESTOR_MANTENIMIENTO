from django.urls import path

from . import views

app_name = "mantenimiento_preventivo"

urlpatterns = [
    path("", views.index, name="index"),
]

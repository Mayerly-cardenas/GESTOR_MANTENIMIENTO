from django.urls import path

from . import views

app_name = "mantenimiento_electrico"

urlpatterns = [
    path("", views.index, name="index"),
]

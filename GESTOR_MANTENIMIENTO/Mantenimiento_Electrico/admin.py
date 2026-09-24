from django.contrib import admin

from .models import RegistroActividad


@admin.register(RegistroActividad)
class RegistroActividadAdmin(admin.ModelAdmin):
    list_display = ("fecha_hora", "operario", "tipo_actividad", "motor", "sala_electrica")
    list_filter = ("tipo_actividad", "sala_electrica")
    search_fields = ("descripcion", "operario__username", "motor__identification_no")
    date_hierarchy = "fecha_hora"

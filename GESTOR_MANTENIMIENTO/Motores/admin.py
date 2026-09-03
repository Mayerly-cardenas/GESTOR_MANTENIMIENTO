from django.contrib import admin

from .models import Fabrica, Fabricante, Motor, SalaElectrica, Ubicacion


@admin.register(Fabricante)
class FabricanteAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(Fabrica)
class FabricaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigo", "fabrica")
    list_filter = ("fabrica",)
    search_fields = ("nombre", "codigo")


@admin.register(SalaElectrica)
class SalaElectricaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "fabrica", "ubicacion")
    list_filter = ("fabrica",)
    search_fields = ("nombre",)


@admin.register(Motor)
class MotorAdmin(admin.ModelAdmin):
    list_display = ("identification_no", "equipment_description", "fabrica", "ubicacion", "evidencia_estado")
    list_filter = ("fabrica", "ubicacion", "sala_electrica")
    search_fields = ("identification_no", "equipment_description", "serial")

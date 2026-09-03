from django.contrib import admin

from .models import Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("user", "rol", "aprobado", "creado_en")
    list_filter = ("rol", "aprobado")
    search_fields = ("user__username", "user__email")

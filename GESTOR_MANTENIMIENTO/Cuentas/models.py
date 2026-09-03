from django.conf import settings
from django.db import models


class Perfil(models.Model):
    ADMINISTRADOR = "administrador"
    MANTENIMIENTO = "mantenimiento"
    ROL_CHOICES = [
        (ADMINISTRADOR, "Administrador"),
        (MANTENIMIENTO, "Mantenimiento"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil"
    )
    rol = models.CharField("Rol", max_length=20, choices=ROL_CHOICES, default=MANTENIMIENTO)
    aprobado = models.BooleanField("Aprobado", default=False)
    creado_en = models.DateTimeField("Creado", auto_now_add=True)

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

    def __str__(self):
        return f"{self.user.get_username()} ({self.get_rol_display()})"

    @property
    def es_administrador(self):
        return self.rol == self.ADMINISTRADOR

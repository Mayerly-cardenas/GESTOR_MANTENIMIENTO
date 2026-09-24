from django.conf import settings
from django.db import models

from Motores.models import Motor, SalaElectrica, Ubicacion


class RegistroActividad(models.Model):
    """Bitácora de trabajos realizados por el personal de mantenimiento eléctrico."""

    INSPECCION = "inspeccion"
    REPARACION = "reparacion"
    CAMBIO_REPUESTO = "cambio_repuesto"
    INSTALACION = "instalacion"
    MEDICION = "medicion"
    OTRO = "otro"
    TIPO_ACTIVIDAD_CHOICES = [
        (INSPECCION, "Inspección"),
        (REPARACION, "Reparación"),
        (CAMBIO_REPUESTO, "Cambio de repuesto"),
        (INSTALACION, "Instalación"),
        (MEDICION, "Medición eléctrica"),
        (OTRO, "Otro"),
    ]

    operario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name="registros_mantenimiento_electrico", verbose_name="Operario",
    )
    motor = models.ForeignKey(
        Motor, on_delete=models.SET_NULL, related_name="registros_actividad",
        verbose_name="Motor", null=True, blank=True,
    )
    ubicacion = models.ForeignKey(
        Ubicacion, on_delete=models.SET_NULL, related_name="registros_actividad",
        verbose_name="Ubicación", null=True, blank=True,
    )
    sala_electrica = models.ForeignKey(
        SalaElectrica, on_delete=models.SET_NULL, related_name="registros_actividad",
        verbose_name="Sala Eléctrica", null=True, blank=True,
    )
    tipo_actividad = models.CharField(
        "Tipo de actividad", max_length=30, choices=TIPO_ACTIVIDAD_CHOICES, default=INSPECCION,
    )
    descripcion = models.TextField("Descripción de la actividad")
    fecha_hora = models.DateTimeField("Fecha y hora", auto_now_add=True)

    class Meta:
        verbose_name = "Registro de actividad"
        verbose_name_plural = "Registros de actividad"
        ordering = ["-fecha_hora"]

    def __str__(self):
        return f"{self.get_tipo_actividad_display()} - {self.operario} ({self.fecha_hora:%d/%m/%Y %H:%M})"

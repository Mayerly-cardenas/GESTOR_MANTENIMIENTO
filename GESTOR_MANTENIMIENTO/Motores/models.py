from django.db import models


class Fabricante(models.Model):
    nombre = models.CharField("Fabricante", max_length=150, unique=True)

    class Meta:
        verbose_name = "Fabricante"
        verbose_name_plural = "Fabricantes"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Fabrica(models.Model):
    nombre = models.CharField("Fábrica", max_length=150, unique=True)

    class Meta:
        verbose_name = "Fábrica"
        verbose_name_plural = "Fábricas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Ubicacion(models.Model):
    fabrica = models.ForeignKey(
        Fabrica, on_delete=models.SET_NULL, related_name="ubicaciones", verbose_name="Fábrica",
        null=True, blank=True,
    )
    nombre = models.CharField("Ubicación", max_length=150, unique=True)
    codigo = models.CharField("Código", max_length=50, blank=True)

    class Meta:
        verbose_name = "Ubicación"
        verbose_name_plural = "Ubicaciones"
        ordering = ["nombre"]

    def __str__(self):
        if self.fabrica:
            return f"{self.nombre} ({self.fabrica.nombre})"
        return self.nombre


class SalaElectrica(models.Model):
    fabrica = models.ForeignKey(
        Fabrica, on_delete=models.SET_NULL, related_name="salas_electricas", verbose_name="Fábrica",
        null=True, blank=True,
    )
    ubicacion = models.ForeignKey(
        Ubicacion, on_delete=models.SET_NULL, related_name="salas_electricas",
        verbose_name="Ubicación", null=True, blank=True,
    )
    nombre = models.CharField("Electrical Room ID", max_length=150, unique=True)

    class Meta:
        verbose_name = "Sala Eléctrica"
        verbose_name_plural = "Salas Eléctricas"
        ordering = ["nombre"]

    def __str__(self):
        if self.fabrica:
            return f"{self.nombre} ({self.fabrica.nombre})"
        return self.nombre


class Motor(models.Model):
    MV_LVD_MCC_CHOICES = [
        ("MV", "MV"),
        ("LVD", "LVD"),
        ("MCC", "MCC"),
    ]

    # Identificación y ubicación
    identification_no = models.CharField("Identification No. (ACS)", max_length=100, unique=True)
    equipment_description = models.CharField("Equipment Description", max_length=255)
    fabrica = models.ForeignKey(
        Fabricante, on_delete=models.SET_NULL, related_name="motores_fabrica", verbose_name="Fábrica",
        null=True, blank=True,
    )
    ubicacion = models.ForeignKey(
        Ubicacion, on_delete=models.PROTECT, related_name="motores", verbose_name="Location ID",
        null=True, blank=True,
    )
    sala_electrica = models.ForeignKey(
        SalaElectrica, on_delete=models.SET_NULL, related_name="motores",
        verbose_name="Electrical Room ID", null=True, blank=True,
    )

    # Potencia y características eléctricas
    power_hp = models.DecimalField("Power Motor HP", max_digits=8, decimal_places=2, null=True, blank=True)
    power_kw = models.DecimalField("Power Motor kW", max_digits=8, decimal_places=2, null=True, blank=True)
    power_kva = models.DecimalField("Power Consumer kVA", max_digits=8, decimal_places=2, null=True, blank=True)
    volt = models.CharField("Volt", max_length=50, blank=True)
    current = models.DecimalField("Current", max_digits=8, decimal_places=2, null=True, blank=True)
    speed_1 = models.CharField("Speed 1 - Speed 2", max_length=100, blank=True)
    starting = models.CharField("Starting", max_length=100, blank=True)
    tipo = models.CharField("Type", max_length=100, blank=True)
    protection_class = models.CharField("Protect. Class", max_length=50, blank=True)
    insul_temp_rise = models.CharField("Insul. Temp. Rise", max_length=50, blank=True)

    # Fabricante y proveedor
    manufacturer_id = models.ForeignKey(
        Fabricante, on_delete=models.PROTECT, related_name="motores",
        verbose_name="Manufacturer ID", null=True, blank=True,
    )
    supplier = models.CharField("Supplier", max_length=150, blank=True)

    # Instalación eléctrica
    mv_lvd_mcc = models.CharField("MV / LVD / MCC", max_length=50, blank=True)
    emergency_power_required = models.BooleanField("Emergency Power Required", default=False)
    pastil_current_a = models.DecimalField("Pastil Current A", max_digits=8, decimal_places=2, null=True, blank=True)
    breaker_current_a = models.DecimalField("Breaker Current A", max_digits=8, decimal_places=2, null=True, blank=True)
    heater_serial = models.CharField("Heater Serial", max_length=100, blank=True)
    heater_current = models.CharField("Heater Current", max_length=100, blank=True)

    # Datos técnicos adicionales
    nema = models.CharField("Nema", max_length=50, blank=True)
    serial = models.CharField("Serial", max_length=100, blank=True)
    mounted = models.CharField("Mounted", max_length=100, blank=True)
    frame = models.CharField("Frame", max_length=50, blank=True)
    torque_nm = models.DecimalField("Torque Nm", max_digits=8, decimal_places=2, null=True, blank=True)
    poles = models.PositiveSmallIntegerField("Poles", null=True, blank=True)
    fs = models.CharField("F.S", max_length=50, blank=True)
    ron_ned_la = models.CharField("Ron NED (LA)", max_length=50, blank=True)
    ron_ed_ll = models.CharField("Ron ED (LL)", max_length=50, blank=True)
    efficiency = models.DecimalField("Efficiency", max_digits=6, decimal_places=2, null=True, blank=True)

    # Evidencia fotográfica
    imagen_motor = models.ImageField("Imagen Motor", upload_to="motores/motor/", null=True, blank=True)
    imagen_placa = models.ImageField("Imagen Placa", upload_to="motores/placa/", null=True, blank=True)
    imagen_switches = models.ImageField("Imagen Switches", upload_to="motores/switches/", null=True, blank=True)

    created_at = models.DateTimeField("Creado", auto_now_add=True)
    updated_at = models.DateTimeField("Actualizado", auto_now=True)

    class Meta:
        verbose_name = "Motor"
        verbose_name_plural = "Motores"
        ordering = ["identification_no"]

    def __str__(self):
        return f"{self.identification_no} - {self.equipment_description}"

    @property
    def evidencia_count(self):
        return sum(1 for img in (self.imagen_motor, self.imagen_placa, self.imagen_switches) if img)

    @property
    def evidencia_estado(self):
        count = self.evidencia_count
        if count == 3:
            return "verde"
        if count in (1, 2):
            return "naranja"
        return "rojo"

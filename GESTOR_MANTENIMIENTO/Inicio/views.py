from django.db.models import Count, Q
from django.utils.safestring import mark_safe
from django.shortcuts import render

from Mantenimiento_Electrico.models import RegistroActividad
from Motores.models import Fabricante, Motor, Ubicacion


def inicio(request):
    motores = Motor.objects.select_related("fabrica", "ubicacion")
    total = motores.count()

    verde = sum(1 for m in motores if m.evidencia_estado == "verde")
    naranja = sum(1 for m in motores if m.evidencia_estado == "naranja")
    rojo = sum(1 for m in motores if m.evidencia_estado == "rojo")

    def pct(value):
        return round((value / total) * 100) if total else 0

    colores_ubicacion = ["#0d6efd", "#13b8d4", "#ec008c", "#ff9800", "#70ad2f", "#5534b5", "#ef476f", "#f45d48"]
    conteo_ubicaciones = {}
    for motor in motores:
        nombre = motor.ubicacion.nombre if motor.ubicacion else "Sin ubicación"
        conteo_ubicaciones[nombre] = conteo_ubicaciones.get(nombre, 0) + 1

    ubicaciones = []
    inicio_segmento = 0
    for indice, (nombre, cantidad) in enumerate(sorted(conteo_ubicaciones.items(), key=lambda item: (-item[1], item[0]))):
        porcentaje = (cantidad / total) * 100 if total else 0
        fin_segmento = inicio_segmento + porcentaje
        color = colores_ubicacion[indice % len(colores_ubicacion)]
        ubicaciones.append({
            "nombre": nombre,
            "total": cantidad,
            "porcentaje": round(porcentaje, 1),
            "color": color,
        })
        inicio_segmento = fin_segmento

    segmentos = ", ".join(
        f"{ubicacion['color']} {inicio:.2f}% {fin:.2f}%"
        for ubicacion, inicio, fin in zip(
            ubicaciones,
            [0] + [sum(item["porcentaje"] for item in ubicaciones[:indice]) for indice in range(1, len(ubicaciones))],
            [sum(item["porcentaje"] for item in ubicaciones[:indice + 1]) for indice in range(len(ubicaciones))],
        )
    )

    fabricas = []
    for fabrica in Fabricante.objects.annotate(total_motores=Count("motores_fabrica")).order_by("nombre"):
        motores_fabrica = list(fabrica.motores_fabrica.all())
        f_total = len(motores_fabrica)
        f_verde = sum(1 for m in motores_fabrica if m.evidencia_estado == "verde")
        f_naranja = sum(1 for m in motores_fabrica if m.evidencia_estado == "naranja")
        f_rojo = sum(1 for m in motores_fabrica if m.evidencia_estado == "rojo")
        if f_total:
            fabricas.append({
                "nombre": fabrica.nombre,
                "total": f_total,
                "verde": f_verde,
                "naranja": f_naranja,
                "rojo": f_rojo,
                "pct_rojo": round((f_rojo / f_total) * 100),
            })

    fabricas.sort(key=lambda fabrica: (-fabrica["total"], fabrica["nombre"]))

    context = {
        "total": total,
        "verde": verde,
        "naranja": naranja,
        "rojo": rojo,
        "pct_verde": pct(verde),
        "pct_naranja": pct(naranja),
        "pct_rojo": pct(rojo),
        "ubicaciones": ubicaciones,
        "ubicaciones_grafico": mark_safe(f"conic-gradient({segmentos})" if segmentos else "#e9ecef"),
        "fabricas": fabricas,
        "fabricas_mostradas": fabricas[:6],
        "fabricas_activas": len(fabricas),
        "fabricas_sin_motores": Fabricante.objects.filter(motores_fabrica__isnull=True).count(),
        "ultimos_motores": motores.order_by("-created_at")[:5],
        "ultimas_actividades": RegistroActividad.objects.select_related(
            "operario", "motor", "sala_electrica"
        )[:5],
        "total_actividades": RegistroActividad.objects.count(),
    }
    return render(request, "inicio.html", context)
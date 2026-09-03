from django.shortcuts import render


def index(request):
    context = {
        "modulo_titulo": "Mantenimiento Preventivo",
        "modulo_icono": "bi-calendar-check",
    }
    return render(request, "Mantenimiento_Preventivo/index.html", context)

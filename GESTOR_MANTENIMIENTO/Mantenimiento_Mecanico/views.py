from django.shortcuts import render


def index(request):
    context = {
        "modulo_titulo": "Mantenimiento Mecánico",
        "modulo_icono": "bi-gear-wide-connected",
    }
    return render(request, "Mantenimiento_Mecanico/index.html", context)

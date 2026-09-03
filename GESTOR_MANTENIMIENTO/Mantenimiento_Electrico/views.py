from django.shortcuts import render


def index(request):
    context = {
        "modulo_titulo": "Mantenimiento Eléctrico",
        "modulo_icono": "bi-lightning-charge",
    }
    return render(request, "Mantenimiento_Electrico/index.html", context)

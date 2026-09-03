from .models import Perfil


def perfil_contexto(request):
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return {}

    es_admin = user.is_superuser or getattr(getattr(user, "perfil", None), "es_administrador", False)
    pendientes = Perfil.objects.filter(aprobado=False).count() if es_admin else 0

    return {
        "es_administrador": es_admin,
        "usuarios_pendientes_count": pendientes,
    }

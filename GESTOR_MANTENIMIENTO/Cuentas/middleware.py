from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect

from .models import Perfil

EXEMPT_PREFIXES = ("/cuentas/", "/admin/", settings.STATIC_URL, settings.MEDIA_URL)


class AccesoMiddleware:
    """Requiere sesión iniciada y aprobación del administrador para usar el sistema."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if not any(prefix and path.startswith(prefix) for prefix in EXEMPT_PREFIXES):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path(), login_url=settings.LOGIN_URL)
            if not request.user.is_superuser:
                perfil = getattr(request.user, "perfil", None)
                if perfil is not None and not perfil.aprobado:
                    return redirect("cuentas:pendiente")
        return self.get_response(request)

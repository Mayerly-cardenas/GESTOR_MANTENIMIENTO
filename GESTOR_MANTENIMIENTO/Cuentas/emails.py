from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse

from .models import Perfil


def _site_url(request):
    if request is not None:
        return f"{request.scheme}://{request.get_host()}"
    return "http://localhost:8000"


def emails_administradores():
    return list(
        User.objects.filter(perfil__rol=Perfil.ADMINISTRADOR, is_active=True, email__gt="")
        .values_list("email", flat=True)
    )


def enviar_solicitud_aprobacion(request, usuario_nuevo):
    destinatarios = emails_administradores()
    if not destinatarios:
        return
    url = _site_url(request) + reverse("cuentas:aprobar_usuarios")
    send_mail(
        subject="HOLCIM GSTOR · Nueva solicitud de acceso pendiente de aprobación",
        message=(
            f"Se registró una nueva solicitud de acceso al sistema.\n\n"
            f"Usuario: {usuario_nuevo.username}\n"
            f"Nombre: {usuario_nuevo.first_name}\n"
            f"Correo: {usuario_nuevo.email}\n\n"
            f"Ingresa al siguiente enlace para revisar y aprobar o rechazar la solicitud:\n{url}\n"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=destinatarios,
        fail_silently=True,
    )


def enviar_aprobacion_usuario(request, usuario):
    if not usuario.email:
        return
    url = _site_url(request) + reverse("cuentas:login")
    send_mail(
        subject="HOLCIM GSTOR · Tu acceso ha sido aprobado",
        message=(
            f"Hola {usuario.first_name or usuario.username},\n\n"
            f"Tu solicitud de acceso al Gestor de Mantenimiento fue aprobada por un administrador.\n"
            f"Ya puedes iniciar sesión con tu usuario: {usuario.username}\n\n"
            f"Ingresa aquí: {url}\n"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[usuario.email],
        fail_silently=True,
    )


def enviar_rechazo_usuario(request, email, username):
    if not email:
        return
    send_mail(
        subject="HOLCIM GSTOR · Solicitud de acceso rechazada",
        message=(
            f"Hola {username},\n\n"
            "Tu solicitud de acceso al Gestor de Mantenimiento fue rechazada por un administrador.\n"
            "Si consideras que esto es un error, contacta a tu administrador."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=True,
    )


def enviar_credenciales_usuario(request, usuario, password):
    if not usuario.email:
        return
    url = _site_url(request) + reverse("cuentas:login")
    send_mail(
        subject="HOLCIM GSTOR · Se creó tu cuenta de acceso",
        message=(
            f"Hola {usuario.first_name or usuario.username},\n\n"
            "Un administrador creó una cuenta de acceso para ti en el Gestor de Mantenimiento.\n\n"
            f"Usuario: {usuario.username}\n"
            f"Contraseña temporal: {password}\n\n"
            f"Ingresa aquí y cambia tu contraseña: {url}\n"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[usuario.email],
        fail_silently=True,
    )

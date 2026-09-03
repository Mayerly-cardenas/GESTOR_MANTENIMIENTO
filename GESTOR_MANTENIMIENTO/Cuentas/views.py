from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render

from . import emails
from .forms import CrearUsuarioForm, LoginForm, RegistroForm
from .models import Perfil


def es_administrador(user):
    return user.is_superuser or getattr(getattr(user, "perfil", None), "es_administrador", False)


class CuentasLoginView(LoginView):
    template_name = "Cuentas/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


def registro(request):
    if request.user.is_authenticated:
        return redirect("inicio")

    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            emails.enviar_solicitud_aprobacion(request, usuario)
            messages.success(
                request,
                "Tu solicitud fue enviada. Un administrador la revisará y te notificaremos "
                "por correo cuando tu cuenta esté aprobada.",
            )
            return redirect("cuentas:login")
    else:
        form = RegistroForm()
    return render(request, "Cuentas/registro.html", {"form": form})


@login_required
def pendiente(request):
    perfil = getattr(request.user, "perfil", None)
    if perfil and perfil.aprobado:
        return redirect("inicio")
    return render(request, "Cuentas/pendiente.html")


@login_required
@user_passes_test(es_administrador)
def aprobar_usuarios(request):
    if request.method == "POST":
        perfil = get_object_or_404(Perfil, pk=request.POST.get("perfil_id"))
        accion = request.POST.get("accion")
        usuario = perfil.user
        if accion == "aprobar":
            perfil.aprobado = True
            perfil.save()
            usuario.is_active = True
            usuario.save()
            emails.enviar_aprobacion_usuario(request, usuario)
            messages.success(request, f"Usuario '{usuario.username}' aprobado correctamente.")
        elif accion == "rechazar":
            correo, nombre = usuario.email, usuario.username
            usuario.delete()
            emails.enviar_rechazo_usuario(request, correo, nombre)
            messages.warning(request, f"Usuario '{nombre}' rechazado y eliminado.")
        return redirect("cuentas:aprobar_usuarios")

    pendientes = Perfil.objects.filter(aprobado=False).select_related("user").order_by("creado_en")
    return render(request, "Cuentas/aprobar_usuarios.html", {"pendientes": pendientes})


@login_required
@user_passes_test(es_administrador)
def lista_usuarios(request):
    usuarios = User.objects.select_related("perfil").order_by("username")
    return render(request, "Cuentas/lista_usuarios.html", {"usuarios": usuarios})


@login_required
@user_passes_test(es_administrador)
def eliminar_usuario(request, pk):
    if request.method != "POST":
        return redirect("cuentas:lista_usuarios")

    usuario = get_object_or_404(User, pk=pk)
    if usuario == request.user:
        messages.error(request, "No puedes eliminar tu propio usuario.")
    elif usuario.is_superuser:
        messages.error(request, "Las cuentas de superusuario no se pueden eliminar desde esta pantalla.")
    else:
        nombre = usuario.username
        usuario.delete()
        messages.success(request, f"Usuario '{nombre}' eliminado correctamente.")
    return redirect("cuentas:lista_usuarios")


@login_required
@user_passes_test(es_administrador)
def crear_usuario(request):
    if request.method == "POST":
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            usuario = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
                first_name=form.cleaned_data["first_name"],
                is_active=True,
            )
            Perfil.objects.filter(user=usuario).update(rol=form.cleaned_data["rol"], aprobado=True)
            emails.enviar_credenciales_usuario(request, usuario, form.cleaned_data["password1"])
            messages.success(request, f"Usuario '{usuario.username}' creado y aprobado correctamente.")
            return redirect("cuentas:lista_usuarios")
    else:
        form = CrearUsuarioForm()
    return render(request, "Cuentas/crear_usuario.html", {"form": form})

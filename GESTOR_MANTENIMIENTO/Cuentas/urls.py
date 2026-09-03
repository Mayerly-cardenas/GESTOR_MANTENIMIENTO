from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "cuentas"

urlpatterns = [
    path("login/", views.CuentasLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="cuentas:login"), name="logout"),
    path("registro/", views.registro, name="registro"),
    path("pendiente/", views.pendiente, name="pendiente"),

    path("usuarios/", views.lista_usuarios, name="lista_usuarios"),
    path("usuarios/crear/", views.crear_usuario, name="crear_usuario"),
    path("usuarios/aprobar/", views.aprobar_usuarios, name="aprobar_usuarios"),
    path("usuarios/<int:pk>/eliminar/", views.eliminar_usuario, name="eliminar_usuario"),

    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="Cuentas/password_reset_form.html",
            email_template_name="Cuentas/password_reset_email.txt",
            subject_template_name="Cuentas/password_reset_subject.txt",
            success_url="/cuentas/password-reset/enviado/",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/enviado/",
        auth_views.PasswordResetDoneView.as_view(template_name="Cuentas/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="Cuentas/password_reset_confirm.html",
            success_url="/cuentas/reset/completado/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/completado/",
        auth_views.PasswordResetCompleteView.as_view(template_name="Cuentas/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Perfil

INPUT_CLASS = "form-control"


class RegistroForm(UserCreationForm):
    first_name = forms.CharField(
        label="Nombre completo", max_length=150,
        widget=forms.TextInput(attrs={"class": INPUT_CLASS}),
    )
    email = forms.EmailField(
        label="Correo electrónico", required=True,
        widget=forms.EmailInput(attrs={"class": INPUT_CLASS}),
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", INPUT_CLASS)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta registrada con este correo.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.is_active = False
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", INPUT_CLASS)

    error_messages = {
        **AuthenticationForm.error_messages,
        "inactive": (
            "Tu cuenta aún no ha sido aprobada por un administrador o fue rechazada. "
            "Te notificaremos por correo cuando puedas ingresar."
        ),
    }


class CrearUsuarioForm(forms.Form):
    username = forms.CharField(label="Usuario", max_length=150, widget=forms.TextInput(attrs={"class": INPUT_CLASS}))
    first_name = forms.CharField(label="Nombre completo", max_length=150, widget=forms.TextInput(attrs={"class": INPUT_CLASS}))
    email = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput(attrs={"class": INPUT_CLASS}))
    rol = forms.ChoiceField(label="Rol", choices=Perfil.ROL_CHOICES, widget=forms.Select(attrs={"class": INPUT_CLASS}))
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={"class": INPUT_CLASS}))
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput(attrs={"class": INPUT_CLASS}))

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Ya existe un usuario con ese nombre.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta registrada con este correo.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get("password1"), cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Las contraseñas no coinciden.")
        return cleaned

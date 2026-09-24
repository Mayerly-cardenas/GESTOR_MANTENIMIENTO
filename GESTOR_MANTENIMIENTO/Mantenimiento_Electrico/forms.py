from django import forms

from .models import RegistroActividad

INPUT_CLASS = "form-control"
SELECT_CLASS = "form-select"


class RegistroActividadForm(forms.ModelForm):
    class Meta:
        model = RegistroActividad
        fields = ["motor", "ubicacion", "sala_electrica", "tipo_actividad", "descripcion"]
        widgets = {
            "motor": forms.Select(attrs={"class": SELECT_CLASS}),
            "ubicacion": forms.Select(attrs={"class": SELECT_CLASS}),
            "sala_electrica": forms.Select(attrs={"class": SELECT_CLASS}),
            "tipo_actividad": forms.Select(attrs={"class": SELECT_CLASS}),
            "descripcion": forms.Textarea(attrs={"class": INPUT_CLASS, "rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["motor"].required = False
        self.fields["ubicacion"].required = False
        self.fields["sala_electrica"].required = False

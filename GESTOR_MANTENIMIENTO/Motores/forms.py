from django import forms

from .models import Fabrica, Fabricante, Motor, SalaElectrica, Ubicacion

INPUT_CLASS = "form-control"
SELECT_CLASS = "form-select"


class FabricanteForm(forms.ModelForm):
    class Meta:
        model = Fabricante
        fields = ["nombre"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": INPUT_CLASS}),
        }


class FabricaForm(forms.ModelForm):
    class Meta:
        model = Fabrica
        fields = ["nombre"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": INPUT_CLASS}),
        }


class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ["fabrica", "nombre", "codigo"]
        widgets = {
            "fabrica": forms.Select(attrs={"class": SELECT_CLASS}),
            "nombre": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "codigo": forms.TextInput(attrs={"class": INPUT_CLASS}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fabrica"].required = False


class SalaElectricaForm(forms.ModelForm):
    class Meta:
        model = SalaElectrica
        fields = ["fabrica", "ubicacion", "nombre"]
        widgets = {
            "fabrica": forms.Select(attrs={"class": SELECT_CLASS}),
            "ubicacion": forms.Select(attrs={"class": SELECT_CLASS}),
            "nombre": forms.TextInput(attrs={"class": INPUT_CLASS}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fabrica"].required = False


class MotorForm(forms.ModelForm):
    class Meta:
        model = Motor
        exclude = ["created_at", "updated_at"]
        widgets = {
            "identification_no": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "equipment_description": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "fabrica": forms.Select(attrs={"class": SELECT_CLASS}),
            "ubicacion": forms.Select(attrs={"class": SELECT_CLASS}),
            "sala_electrica": forms.Select(attrs={"class": SELECT_CLASS}),
            "power_hp": forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01"}),
            "power_kw": forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01"}),
            "power_kva": forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01"}),
            "volt": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "current": forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01"}),
            "speed_1": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "starting": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "tipo": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "protection_class": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "insul_temp_rise": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "manufacturer_id": forms.Select(attrs={"class": SELECT_CLASS}),
            "supplier": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "mv_lvd_mcc": forms.TextInput(attrs={"class": INPUT_CLASS, "list": "mv_lvd_mcc_options"}),
            "emergency_power_required": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "pastil_current_a": forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01"}),
            "breaker_current_a": forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01"}),
            "heater_serial": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "heater_current": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "nema": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "serial": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "mounted": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "frame": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "torque_nm": forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01"}),
            "poles": forms.NumberInput(attrs={"class": INPUT_CLASS}),
            "fs": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "ron_ned_la": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "ron_ed_ll": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "efficiency": forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01"}),
            "imagen_motor": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "imagen_placa": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "imagen_switches": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fabrica"].queryset = Fabricante.objects.order_by("nombre")
        self.fields["fabrica"].required = False
        self.fields["ubicacion"].queryset = Ubicacion.objects.select_related("fabrica")
        self.fields["ubicacion"].required = False
        self.fields["sala_electrica"].queryset = SalaElectrica.objects.select_related("fabrica")
        self.fields["sala_electrica"].required = False
        self.fields["manufacturer_id"].queryset = Fabricante.objects.order_by("nombre")
        self.fields["manufacturer_id"].required = False

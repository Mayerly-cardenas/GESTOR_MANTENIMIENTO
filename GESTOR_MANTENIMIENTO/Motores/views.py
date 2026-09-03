from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import FabricaForm, FabricanteForm, MotorForm, SalaElectricaForm, UbicacionForm
from .models import Fabrica, Fabricante, Motor, SalaElectrica, Ubicacion

class MotorListView(ListView):
    model = Motor
    template_name = "Motores/motor_list.html"
    context_object_name = "motores"
    paginate_by = 20

    def get_queryset(self):
        qs = Motor.objects.select_related("fabrica", "ubicacion", "sala_electrica")
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(identification_no__icontains=query) | qs.filter(
                equipment_description__icontains=query
            )
        estado = self.request.GET.get("evidencia")
        tiene_motor = Q(imagen_motor__isnull=False) & ~Q(imagen_motor="")
        tiene_placa = Q(imagen_placa__isnull=False) & ~Q(imagen_placa="")
        tiene_switches = Q(imagen_switches__isnull=False) & ~Q(imagen_switches="")
        completa = tiene_motor & tiene_placa & tiene_switches
        ninguna = ~tiene_motor & ~tiene_placa & ~tiene_switches
        if estado == "verde":
            qs = qs.filter(completa)
        elif estado == "naranja":
            qs = qs.filter(~completa & ~ninguna)
        elif estado == "rojo":
            qs = qs.filter(ninguna)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        context["evidencia"] = self.request.GET.get("evidencia", "")
        context["total_verde"] = sum(1 for m in self.get_queryset() if m.evidencia_estado == "verde")
        context["total_naranja"] = sum(1 for m in self.get_queryset() if m.evidencia_estado == "naranja")
        context["total_rojo"] = sum(1 for m in self.get_queryset() if m.evidencia_estado == "rojo")
        return context


class MotorDetailView(DetailView):
    model = Motor
    template_name = "Motores/motor_detail.html"
    context_object_name = "motor"


class MotorCreateView(SuccessMessageMixin, CreateView):
    model = Motor
    form_class = MotorForm
    template_name = "Motores/motor_form.html"
    success_url = reverse_lazy("motores:motor_list")
    success_message = "Motor registrado correctamente."


class MotorUpdateView(SuccessMessageMixin, UpdateView):
    model = Motor
    form_class = MotorForm
    template_name = "Motores/motor_form.html"
    success_url = reverse_lazy("motores:motor_list")
    success_message = "Motor actualizado correctamente."


class MotorDeleteView(DeleteView):
    model = Motor
    template_name = "Motores/motor_confirm_delete.html"
    success_url = reverse_lazy("motores:motor_list")

    def form_valid(self, form):
        messages.success(self.request, "Motor eliminado correctamente.")
        return super().form_valid(form)


class FabricanteListView(ListView):
    model = Fabricante
    template_name = "Motores/fabricante_list.html"
    context_object_name = "fabricantes"

    def get_queryset(self):
        qs = Fabricante.objects.prefetch_related("motores")
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(nombre__icontains=query)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        return context


class FabricanteCreateView(SuccessMessageMixin, CreateView):
    model = Fabricante
    form_class = FabricanteForm
    template_name = "Motores/fabricante_form.html"
    success_url = reverse_lazy("motores:fabricante_list")
    success_message = "Fabricante creado correctamente."


class FabricanteUpdateView(SuccessMessageMixin, UpdateView):
    model = Fabricante
    form_class = FabricanteForm
    template_name = "Motores/fabricante_form.html"
    success_url = reverse_lazy("motores:fabricante_list")
    success_message = "Fabricante actualizado correctamente."


class FabricanteDeleteView(DeleteView):
    model = Fabricante
    template_name = "Motores/fabricante_confirm_delete.html"
    success_url = reverse_lazy("motores:fabricante_list")


class FabricaListView(ListView):
    model = Fabrica
    template_name = "Motores/fabrica_list.html"
    context_object_name = "fabricas"


class FabricaCreateView(SuccessMessageMixin, CreateView):
    model = Fabrica
    form_class = FabricaForm
    template_name = "Motores/fabrica_form.html"
    success_url = reverse_lazy("motores:fabrica_list")
    success_message = "Fábrica creada correctamente."


class FabricaUpdateView(SuccessMessageMixin, UpdateView):
    model = Fabrica
    form_class = FabricaForm
    template_name = "Motores/fabrica_form.html"
    success_url = reverse_lazy("motores:fabrica_list")
    success_message = "Fábrica actualizada correctamente."


class FabricaDeleteView(DeleteView):
    model = Fabrica
    template_name = "Motores/fabrica_confirm_delete.html"
    success_url = reverse_lazy("motores:fabrica_list")


class UbicacionListView(ListView):
    model = Ubicacion
    template_name = "Motores/ubicacion_list.html"
    context_object_name = "ubicaciones"

    def get_queryset(self):
        qs = Ubicacion.objects.select_related("fabrica").prefetch_related("motores")
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(nombre__icontains=query)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        return context


class UbicacionCreateView(SuccessMessageMixin, CreateView):
    model = Ubicacion
    form_class = UbicacionForm
    template_name = "Motores/ubicacion_form.html"
    success_url = reverse_lazy("motores:ubicacion_list")
    success_message = "Ubicación creada correctamente."


class UbicacionUpdateView(SuccessMessageMixin, UpdateView):
    model = Ubicacion
    form_class = UbicacionForm
    template_name = "Motores/ubicacion_form.html"
    success_url = reverse_lazy("motores:ubicacion_list")
    success_message = "Ubicación actualizada correctamente."


class UbicacionDeleteView(DeleteView):
    model = Ubicacion
    template_name = "Motores/ubicacion_confirm_delete.html"
    success_url = reverse_lazy("motores:ubicacion_list")


class SalaElectricaListView(ListView):
    model = SalaElectrica
    template_name = "Motores/sala_list.html"
    context_object_name = "salas"

    def get_queryset(self):
        qs = SalaElectrica.objects.select_related("fabrica", "ubicacion").prefetch_related("motores")
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(nombre__icontains=query)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        return context


class SalaElectricaCreateView(SuccessMessageMixin, CreateView):
    model = SalaElectrica
    form_class = SalaElectricaForm
    template_name = "Motores/sala_form.html"
    success_url = reverse_lazy("motores:sala_list")
    success_message = "Sala eléctrica creada correctamente."


class SalaElectricaUpdateView(SuccessMessageMixin, UpdateView):
    model = SalaElectrica
    form_class = SalaElectricaForm
    template_name = "Motores/sala_form.html"
    success_url = reverse_lazy("motores:sala_list")
    success_message = "Sala eléctrica actualizada correctamente."


class SalaElectricaDeleteView(DeleteView):
    model = SalaElectrica
    template_name = "Motores/sala_confirm_delete.html"
    success_url = reverse_lazy("motores:sala_list")


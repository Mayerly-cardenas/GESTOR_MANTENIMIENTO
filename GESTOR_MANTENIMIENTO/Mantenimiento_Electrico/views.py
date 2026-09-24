from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from .forms import RegistroActividadForm
from .models import RegistroActividad


class RegistroActividadListView(LoginRequiredMixin, ListView):
    model = RegistroActividad
    template_name = "Mantenimiento_Electrico/index.html"
    context_object_name = "registros"
    paginate_by = 20

    def get_queryset(self):
        qs = RegistroActividad.objects.select_related(
            "operario", "motor", "ubicacion", "sala_electrica"
        )
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(descripcion__icontains=query)
        tipo = self.request.GET.get("tipo")
        if tipo:
            qs = qs.filter(tipo_actividad=tipo)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        context["tipo"] = self.request.GET.get("tipo", "")
        context["tipos_actividad"] = RegistroActividad.TIPO_ACTIVIDAD_CHOICES
        context["total_registros"] = RegistroActividad.objects.count()
        return context


class RegistroActividadDetailView(LoginRequiredMixin, DetailView):
    model = RegistroActividad
    template_name = "Mantenimiento_Electrico/registro_detail.html"
    context_object_name = "registro"


class RegistroActividadCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = RegistroActividad
    form_class = RegistroActividadForm
    template_name = "Mantenimiento_Electrico/registro_form.html"
    success_url = reverse_lazy("mantenimiento_electrico:index")
    success_message = "Actividad registrada correctamente."

    def form_valid(self, form):
        form.instance.operario = self.request.user
        return super().form_valid(form)


class EsAdministradorMixin(UserPassesTestMixin):
    def test_func(self):
        perfil = getattr(self.request.user, "perfil", None)
        return bool(perfil and perfil.es_administrador)


class RegistroActividadDeleteView(LoginRequiredMixin, EsAdministradorMixin, DeleteView):
    model = RegistroActividad
    template_name = "Mantenimiento_Electrico/registro_confirm_delete.html"
    success_url = reverse_lazy("mantenimiento_electrico:index")

    def form_valid(self, form):
        messages.success(self.request, "Registro eliminado correctamente.")
        return super().form_valid(form)

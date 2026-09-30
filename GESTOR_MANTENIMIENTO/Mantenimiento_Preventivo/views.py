from django.shortcuts import render


def index(request):
	return render(request, 'Mantenimiento_Modulos/index.html', {
		'titulo': 'Mantenimiento Preventivo',
		'icono': 'bi-calendar2-check',
		'descripcion': 'Planificación y seguimiento del mantenimiento preventivo.',
	})

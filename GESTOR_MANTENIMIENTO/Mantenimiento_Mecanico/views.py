from django.shortcuts import render


def index(request):
	return render(request, 'Mantenimiento_Modulos/index.html', {
		'titulo': 'Mantenimiento Mecánico',
		'icono': 'bi-gear-wide-connected',
		'descripcion': 'Gestión de actividades y equipos de mantenimiento mecánico.',
	})

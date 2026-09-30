# Gestor de Mantenimiento

Aplicación web para consultar y administrar información de motores y registrar actividades de mantenimiento de una planta. El sistema está construido con Django y ofrece una interfaz en español para el trabajo diario del personal de mantenimiento y administración.

Este documento explica qué hace el proyecto, cómo está organizado, cómo ejecutarlo en desarrollo y qué funciones todavía están pendientes. La carpeta del proyecto Django es `GESTOR_MANTENIMIENTO/`; el archivo de dependencias y el entorno virtual existente están en la raíz del repositorio.

## Contenido

- [Alcance del sistema](#alcance-del-sistema)
- [Módulos](#módulos)
- [Acceso y roles](#acceso-y-roles)
- [Tecnologías y arquitectura](#tecnologías-y-arquitectura)
- [Requisitos y puesta en marcha](#requisitos-y-puesta-en-marcha)
- [Configuración](#configuración)
- [Rutas principales](#rutas-principales)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Pruebas y mantenimiento](#pruebas-y-mantenimiento)
- [Seguridad y datos locales](#seguridad-y-datos-locales)
- [Estado y próximos pasos](#estado-y-próximos-pasos)

## Alcance del sistema

El proyecto reúne un inventario técnico de motores, información de ubicación, evidencias fotográficas y una bitácora de actividades eléctricas. El dashboard proporciona una vista resumida del inventario y de las actividades recientes.

La interfaz también incluye accesos a Mantenimiento Mecánico y Mantenimiento Preventivo. Actualmente esos dos módulos muestran páginas informativas de entrada; todavía no implementan registro de órdenes, programación preventiva ni seguimiento de tareas.

## Módulos

### Inicio

La página `/` es el dashboard. Presenta indicadores del inventario, distribución por ubicación, estado de las fotografías requeridas, los motores agregados recientemente y las últimas actividades eléctricas.

### Cuentas

La aplicación `Cuentas` gestiona el inicio de sesión, registro de usuarios, aprobación de solicitudes, creación y administración de cuentas, y recuperación de contraseña. Los perfiles distinguen usuarios de mantenimiento y administradores.

### Motores

La aplicación `Motores` gestiona motores y sus datos relacionados: fabricantes, fábricas, ubicaciones y salas eléctricas. Las pantallas disponibles permiten consultar, buscar y administrar estos registros.

Los motores incluyen especificaciones técnicas y tres campos de evidencia fotográfica: imagen del motor, placa y switches. El estado de evidencia se calcula así:

| Estado | Evidencia cargada |
| --- | --- |
| Verde | Las tres imágenes |
| Naranja | Una o dos imágenes |
| Rojo | Ninguna imagen |

Las imágenes subidas se almacenan bajo `media/motores/` durante el desarrollo.

### Mantenimiento Eléctrico

La aplicación `Mantenimiento_Electrico` ofrece una bitácora de actividades. Cada registro guarda el operario, el tipo y descripción del trabajo, la fecha y hora, y puede vincularse opcionalmente con un motor, ubicación o sala eléctrica. Se puede consultar, filtrar, crear y abrir el detalle de las actividades; la eliminación está restringida a administradores.

### Mantenimiento Mecánico y Preventivo

Las aplicaciones `Mantenimiento_Mecanico` y `Mantenimiento_Preventivo` ya están instaladas y cuentan con rutas propias y accesos desde la interfaz. Por ahora cada una presenta una página de entrada compartida que informa que las funciones específicas están pendientes de desarrollo. No se deben considerar todavía módulos operativos de órdenes mecánicas o planes preventivos.

## Acceso y roles

- El inicio de sesión está disponible en `/cuentas/login/`.
- El autorregistro crea una cuenta pendiente de aprobación; un administrador puede aprobarla o rechazarla.
- Los administradores pueden crear usuarios directamente.
- El middleware de acceso exige autenticación y aprobación para la aplicación. Las rutas de cuentas, administración Django, archivos estáticos y archivos multimedia tienen excepciones para permitir autenticación y recursos del sitio.
- La eliminación de actividades eléctricas y la administración de usuarios son acciones restringidas a administradores.

Las restricciones deben revisarse junto con las vistas y permisos antes de desplegar o ampliar los roles; no se debe asumir que todas las operaciones tienen permisos específicos por módulo.

## Tecnologías y arquitectura

- Python y Django; las versiones declaradas del proyecto están en `requirements.txt`.
- SQLite para desarrollo local (`GESTOR_MANTENIMIENTO/db.sqlite3`).
- Plantillas Django para la interfaz, archivos estáticos CSS/JavaScript e imágenes cargadas por usuarios.
- Pillow para el manejo de imágenes.
- Envío de correo configurable por variables de entorno. Sin credenciales SMTP, el proyecto utiliza el backend de consola de Django durante el desarrollo.

Las rutas raíz del proyecto se configuran en `GESTOR_MANTENIMIENTO/Mantenimiento/urls.py`; la configuración general, middleware, plantillas, base de datos y correo están en `GESTOR_MANTENIMIENTO/Mantenimiento/settings.py`.

## Requisitos y puesta en marcha

Los siguientes pasos son para Windows PowerShell. **Se reutiliza el entorno virtual existente `.venv/` en la raíz del repositorio; no hace falta crear otro.** Ejecuta los comandos desde la carpeta raíz del repositorio.

1. Activa el entorno virtual:

	```powershell
	.\.venv\Scripts\Activate.ps1
	```

2. `requirements.txt` está guardado en UTF-16. Si necesitas instalar o actualizar las dependencias, conviértelo a un archivo temporal UTF-8 para que `pip` pueda leerlo:

	```powershell
	$requirementsUtf8 = Join-Path $env:TEMP 'gestor-mantenimiento-requirements.txt'
	Get-Content .\requirements.txt -Encoding Unicode | Set-Content $requirementsUtf8 -Encoding utf8
	python -m pip install -r $requirementsUtf8
	Remove-Item $requirementsUtf8
	```

3. Entra a la carpeta Django y aplica las migraciones:

	```powershell
	Set-Location .\GESTOR_MANTENIMIENTO
	python manage.py migrate
	```

4. Opcionalmente, crea un usuario administrador si la base de datos aún no tiene uno:

	```powershell
	python manage.py createsuperuser
	```

5. Inicia el servidor de desarrollo:

	```powershell
	python manage.py runserver
	```

6. Abre <http://127.0.0.1:8000/> en el navegador. El panel administrativo de Django está en <http://127.0.0.1:8000/admin/>.

Para detener el servidor, usa `Ctrl+C` en la terminal. Los comandos Django posteriores se ejecutan desde `GESTOR_MANTENIMIENTO/` con el mismo entorno activo.

## Configuración

La configuración de correo lee estas variables de entorno:

| Variable | Uso |
| --- | --- |
| `EMAIL_HOST_USER` | Usuario SMTP; si falta, se usa la salida por consola. |
| `EMAIL_HOST_PASSWORD` | Contraseña SMTP; se requiere junto al usuario para activar SMTP. |
| `EMAIL_HOST` | Servidor SMTP; valor predeterminado configurado: `smtp.gmail.com`. |
| `EMAIL_PORT` | Puerto SMTP; valor predeterminado: `587`. |
| `EMAIL_USE_TLS` | Activa TLS; valor predeterminado: `True`. |
| `DEFAULT_FROM_EMAIL` | Remitente de los correos. |

Las variables se leen directamente del entorno del proceso. El proyecto no carga automáticamente un archivo `.env`.

## Rutas principales

| Sección | Ruta | Funcionalidad |
| --- | --- | --- |
| Dashboard | `/` | Resumen del sistema. |
| Administración Django | `/admin/` | Sitio administrativo de Django. |
| Cuentas | `/cuentas/login/` | Inicio de sesión. |
| Cuentas | `/cuentas/registro/` | Solicitud de registro de usuario. |
| Cuentas | `/cuentas/pendiente/` | Estado de aprobación pendiente. |
| Cuentas | `/cuentas/usuarios/` | Administración de usuarios. |
| Cuentas | `/cuentas/usuarios/crear/` | Creación de cuentas por administradores. |
| Cuentas | `/cuentas/usuarios/aprobar/` | Aprobación o rechazo de solicitudes. |
| Cuentas | `/cuentas/password-reset/` | Inicio de recuperación de contraseña. |
| Motores | `/motores/` | Inventario de motores. |
| Datos relacionados | `/motores/fabricantes/` | Fabricantes. |
| Datos relacionados | `/motores/fabricas/` | Fábricas. |
| Datos relacionados | `/motores/ubicaciones/` | Ubicaciones. |
| Datos relacionados | `/motores/salas-electricas/` | Salas eléctricas. |
| Mantenimiento eléctrico | `/mantenimiento-electrico/` | Lista de actividades. |
| Mantenimiento eléctrico | `/mantenimiento-electrico/nuevo/` | Registro de una actividad. |
| Mantenimiento mecánico | `/mantenimiento-mecanico/` | Página de entrada; funciones por implementar. |
| Mantenimiento preventivo | `/mantenimiento-preventivo/` | Página de entrada; funciones por implementar. |

Las secciones de motores y sus datos relacionados incluyen rutas de creación, edición, detalle o eliminación según el tipo de registro. Las rutas exactas están definidas en `Motores/urls.py`.

## Estructura del repositorio

```text
.
├── README.md
├── requirements.txt
├── .venv/                        # Entorno virtual existente; no versionar
└── GESTOR_MANTENIMIENTO/
	 ├── manage.py
	 ├── db.sqlite3                # Base de datos local de desarrollo
	 ├── Mantenimiento/            # Settings y rutas principales
	 ├── Cuentas/                  # Autenticación, perfiles y aprobaciones
	 ├── Inicio/                   # Dashboard
	 ├── Motores/                  # Inventario, formularios, vistas y plantillas
	 ├── Mantenimiento_Electrico/  # Bitácora eléctrica
	 ├── Mantenimiento_Mecanico/   # Página de entrada del módulo
	 ├── Mantenimiento_Preventivo/ # Página de entrada del módulo
	 ├── templates/                # Plantillas compartidas
	 ├── static/                  # Recursos estáticos del sitio
	 └── media/                   # Evidencias fotográficas locales
```

Cada aplicación Django tiene sus propias vistas, rutas, modelos y migraciones cuando corresponde. El estilo global de la interfaz y la navegación compartida se encuentran principalmente en los recursos de `Motores/`.

## Pruebas y mantenimiento

Desde `GESTOR_MANTENIMIENTO/`, con el entorno existente activo:

```powershell
python manage.py check
python manage.py test
```

`check` valida la configuración del proyecto. `test` ejecuta las pruebas Django disponibles. La cobertura actual es limitada; revisa los resultados del comando antes de considerar un cambio verificado. `_test_login.py` es un script manual de prueba HTTP y no sustituye a la suite de pruebas Django.

Estado comprobado en este entorno: `python manage.py check` pasa. `python manage.py test` descubre una prueba y actualmente falla en `Motores.tests.MotorAuditTest.test_update_records_authenticated_user_and_timestamp`: el doble de formulario `MotorFormStub` no tiene el atributo `cleaned_data` que utiliza `SuccessMessageMixin`. Esta falla está pendiente de corrección.

Al modificar modelos, genera migraciones y aplícalas:

```powershell
python manage.py makemigrations
python manage.py migrate
```

No borres la base de datos ni las imágenes locales como parte de una prueba rutinaria: pueden contener información que se debe conservar.

## Seguridad y datos locales

- La configuración actual de desarrollo tiene `DEBUG` activado y contiene una clave secreta definida en settings. No copies claves ni contraseñas en este README, en el código o en commits. Antes de desplegar, mueve la clave a una variable de entorno, rota cualquier clave que haya sido expuesta, desactiva `DEBUG` y configura `ALLOWED_HOSTS`.
- Usa SMTP mediante variables de entorno y evita guardar credenciales reales en el repositorio o en archivos compartidos.
- `db.sqlite3` y `media/` pueden contener información operativa y fotografías. Trátalos como datos locales potencialmente sensibles y respáldalos de forma controlada.
- Verifica qué archivos se van a incluir en Git antes de publicar cambios; no subas bases de datos, credenciales, archivos multimedia privados ni el entorno virtual.
- El servidor integrado de Django es para desarrollo, no para producción.

## Estado y próximos pasos

Actualmente están implementados el inventario de motores, el dashboard, el control de cuentas y la bitácora eléctrica. Las áreas mecánica y preventiva están visibles e integradas en la navegación, pero sus procesos funcionales están pendientes.

Posibles siguientes entregas para completar el sistema:

- Definir los campos, estados y permisos de las órdenes de mantenimiento mecánico.
- Diseñar planes, frecuencias, calendario y registro de ejecución para mantenimiento preventivo.
- Ampliar pruebas automatizadas para autenticación, permisos, inventario y actividades.
- Completar la configuración de producción: secretos externos, hosts permitidos, base de datos, almacenamiento de medios y servidor de aplicaciones.

Las funciones descritas como pendientes no deben presentarse como disponibles hasta que se implementen y se prueben.

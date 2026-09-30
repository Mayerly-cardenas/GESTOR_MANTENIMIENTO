# Gestor de Mantenimiento

Aplicación web desarrollada con Django para administrar motores y consultar las actividades de mantenimiento de la planta. El repositorio del proyecto está en `GESTOR_MANTENIMIENTO/`; el archivo de dependencias está un nivel arriba, en `requirements.txt`.

## Requisitos

- Windows y PowerShell.
- Python compatible con las versiones declaradas en `../requirements.txt`.
- El entorno virtual existente en `../venv/`.

No es necesario crear otro entorno virtual. Los ejemplos siguientes se ejecutan desde la carpeta `GESTOR_MANTENIMIENTO`.

## Preparación y ejecución

Activa el entorno existente:

```powershell
..\venv\Scripts\Activate.ps1
```

Si las dependencias todavía no están instaladas en ese entorno, `requirements.txt` está guardado en UTF-16. Convierte su contenido a un archivo temporal UTF-8 para instalarlo:

```powershell
Get-Content ..\requirements.txt -Encoding Unicode | Set-Content requirements-utf8.txt -Encoding utf8
python -m pip install -r requirements-utf8.txt
Remove-Item requirements-utf8.txt
```

Aplica las migraciones y arranca el servidor de desarrollo:

```powershell
python manage.py migrate
python manage.py runserver
```

Abre <http://127.0.0.1:8000/>. Para entrar al panel de administración de Django, crea una cuenta de administrador si aún no existe:

```powershell
python manage.py createsuperuser
```

Comprobaciones útiles:

```powershell
python manage.py check
python manage.py test
```

## Módulos y rutas

| Área | Ruta | Estado actual |
| --- | --- | --- |
| Inicio | `/` | Dashboard con indicadores de motores, estado de evidencias y últimas actividades eléctricas. |
| Cuentas | `/cuentas/login/` | Inicio de sesión, registro, aprobación de usuarios, administración de cuentas y recuperación de contraseña. |
| Motores | `/motores/` | Gestión de motores, fabricantes, fábricas, ubicaciones y salas eléctricas; incluye evidencias fotográficas. |
| Mantenimiento eléctrico | `/mantenimiento-electrico/` | Bitácora de actividades con consulta, creación, detalle y eliminación restringida a administradores. |
| Mantenimiento mecánico | `/mantenimiento-mecanico/` | Página de entrada integrada; sus funciones específicas están pendientes de desarrollo. |
| Mantenimiento preventivo | `/mantenimiento-preventivo/` | Página de entrada integrada; sus funciones específicas están pendientes de desarrollo. |
| Administración Django | `/admin/` | Administración estándar de Django. |

Las páginas de mecánico y preventivo ya están registradas en la configuración y enlazadas desde el dashboard, pero por ahora no incluyen gestión de órdenes, planes o tareas.

## Estructura principal

- `Mantenimiento/`: configuración global y enrutamiento del proyecto.
- `Cuentas/`: autenticación, perfiles, aprobación y permisos de usuarios.
- `Inicio/`: dashboard principal.
- `Motores/`: modelos, vistas y formularios para el inventario de motores y sus datos relacionados.
- `Mantenimiento_Electrico/`: bitácora de trabajos eléctricos.
- `Mantenimiento_Mecanico/`: punto de entrada del módulo mecánico.
- `Mantenimiento_Preventivo/`: punto de entrada del módulo preventivo.
- `templates/`: plantillas compartidas del sitio.
- `static/`: archivos estáticos globales.
- `media/`: fotografías cargadas para los motores.
- `db.sqlite3`: base de datos SQLite local de desarrollo.
- `../requirements.txt`: dependencias Python del proyecto.
- `../venv/`: entorno virtual existente; no se debe recrear para trabajar con este proyecto.

## Correo electrónico

La configuración de correo lee variables de entorno. Si no se proporcionan credenciales SMTP, Django utiliza la salida por consola durante el desarrollo.

Variables reconocidas: `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS` y `DEFAULT_FROM_EMAIL`. No guardes credenciales ni claves secretas en el repositorio.

## Notas de desarrollo y seguridad

- La base de datos SQLite y las imágenes en `media/` contienen datos locales; respáldalos antes de cambiar de equipo o limpiar el entorno.
- `DEBUG` está activado en la configuración actual. Antes de desplegar, configura un `SECRET_KEY` seguro fuera del repositorio, define `ALLOWED_HOSTS` y sigue la lista de despliegue de Django.
- La configuración de correo usa `os.getenv`; un archivo `.env` no se carga automáticamente.
- Las dependencias exactas se mantienen en `../requirements.txt`. Consulta ese archivo al preparar o actualizar el entorno existente.

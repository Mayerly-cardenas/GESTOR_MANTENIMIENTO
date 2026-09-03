from django.db import migrations

SALAS_ELECTRICAS = [
    "Base 2", "Bedeschi", "Cabina 211-AD1", "Crudo", "Descarga", "Descarga Horno",
    "Elec. Rom", "Enfriador", "Hazemag", "Molino 1", "Molino 2", "Molino 3",
    "N.A", "Prensa", "Reclamo", "Silo 15K", "Torre",
]


def crear_salas_electricas(apps, schema_editor):
    SalaElectrica = apps.get_model("Motores", "SalaElectrica")
    for nombre in SALAS_ELECTRICAS:
        SalaElectrica.objects.get_or_create(nombre=nombre)


def eliminar_salas_electricas(apps, schema_editor):
    SalaElectrica = apps.get_model("Motores", "SalaElectrica")
    SalaElectrica.objects.filter(nombre__in=SALAS_ELECTRICAS, fabrica__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("Motores", "0004_alter_salaelectrica_options_and_more"),
    ]

    operations = [
        migrations.RunPython(crear_salas_electricas, eliminar_salas_electricas),
    ]

from django.db import migrations

FABRICANTES = [
    "BAUER", "SEW EURODRIVE", "WESTERN ELECTRIC", "TOSHIBA", "SIEMENS", "LAFERT",
    "HALTER", "ABB", "LOHER", "FLENDER", "U.S. ELECTRICAL MOTORS", "BALDOR",
    "US MOTORS", "SUMITOMO", "AEG", "GRUNDFOS", "WEG", "VIMARC", "GE", "AUMA",
    "STOBER", "GENERAL ELECTRIC", "MARATHON", "ALIMAK", "G", "ATB", "KATT",
    "BIRKENBEUL", "SIMO MOTORS", "OPTIM", "RELIANCE ELECTRIC", "MARATON ELECTRIC",
    "LEROY SOMER", "BALDOR. RELIANCE", "BROOK CROMPTON", "WOLONG", "DUCHI",
    "TECHTOP", "CROMPTOM GREAVES", "BBC BROWN BOVERI", "GARBE,LAHMEYER & CO",
    "ZIELH-ABEGG", "INNOMOTICS", "MAG", "BTS", "ATB SCHORCH", "BROWN BOVERI",
    "HELMKE", "GRACO", "GEBR. STEIMEL GMBH & CO",
    "KUERLE ANTRIEBSSYSTEME STUTTGART UND HEMMINGEN", "LAMMERS", "FLENDER HIMMEL",
    "WNM", "WNN", "SEW", "TRANSMISIONES", "EMERSON MOTOR COMPANY", "EURODRIVE",
    "MOTORS MARATHON", "Betr&Wart", "LEESON ELECTRIC", "AERZENER", "FLENCO",
    "MARELLI MOTORI", "MGM", "COMES", "WESTHINGHOUSE", "NORD",
]


def crear_fabricantes(apps, schema_editor):
    Fabricante = apps.get_model("Motores", "Fabricante")
    for nombre in FABRICANTES:
        Fabricante.objects.get_or_create(nombre=nombre)


def eliminar_fabricantes(apps, schema_editor):
    Fabricante = apps.get_model("Motores", "Fabricante")
    Fabricante.objects.filter(nombre__in=FABRICANTES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("Motores", "0002_fabricante_alter_motor_mv_lvd_mcc_and_more"),
    ]

    operations = [
        migrations.RunPython(crear_fabricantes, eliminar_fabricantes),
    ]

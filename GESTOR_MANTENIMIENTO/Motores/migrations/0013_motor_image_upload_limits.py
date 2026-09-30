import Motores.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Motores", "0012_motor_actualizado_por"),
    ]

    operations = [
        migrations.AlterField(
            model_name="motor",
            name="imagen_motor",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="motores/motor/",
                validators=[Motores.models.validate_image_size],
                verbose_name="Imagen Motor",
            ),
        ),
        migrations.AlterField(
            model_name="motor",
            name="imagen_placa",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="motores/placa/",
                validators=[Motores.models.validate_image_size],
                verbose_name="Imagen Placa",
            ),
        ),
        migrations.AlterField(
            model_name="motor",
            name="imagen_switches",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="motores/switches/",
                validators=[Motores.models.validate_image_size],
                verbose_name="Imagen Switches",
            ),
        ),
    ]
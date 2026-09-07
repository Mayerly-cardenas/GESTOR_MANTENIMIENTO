from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Motores", "0011_alter_motor_heater_current_alter_motor_ubicacion"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="motor",
            name="actualizado_por",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="motores_actualizados",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Actualizado por",
            ),
        ),
    ]
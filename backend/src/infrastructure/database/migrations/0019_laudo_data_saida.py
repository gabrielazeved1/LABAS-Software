from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0018_finalize_laudo_fk"),
    ]

    operations = [
        migrations.AddField(
            model_name="laudo",
            name="data_saida",
            field=models.DateField(blank=True, null=True, verbose_name="Data de Saída"),
        ),
        migrations.AlterField(
            model_name="laudo",
            name="data_emissao",
            field=models.DateField(
                auto_now_add=False,
                verbose_name="Data de Entrada",
            ),
        ),
    ]

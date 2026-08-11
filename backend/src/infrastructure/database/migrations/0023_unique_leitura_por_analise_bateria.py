import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0022_cleanup_leituras_duplicadas"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="leituraequipamento",
            options={
                "verbose_name": "Leitura de Equipamento",
                "verbose_name_plural": "Leituras de Equipamento",
            },
        ),
        migrations.AlterField(
            model_name="analisesolo",
            name="data_entrada",
            field=models.DateField(default=datetime.date.today, verbose_name="Data Entrada"),
        ),
        migrations.AlterField(
            model_name="bateriacalibracao",
            name="coeficiente_angular_a",
            field=models.DecimalField(
                blank=True,
                decimal_places=8,
                max_digits=15,
                null=True,
                verbose_name="Inclinação (a) — slope",
            ),
        ),
        migrations.AlterField(
            model_name="bateriacalibracao",
            name="coeficiente_linear_b",
            field=models.DecimalField(
                blank=True,
                decimal_places=8,
                max_digits=15,
                null=True,
                verbose_name="Intercepto (b) — intercept",
            ),
        ),
        migrations.AlterField(
            model_name="bateriacalibracao",
            name="equipamento",
            field=models.CharField(
                choices=[
                    ("AA", "Absorcao Atomica"),
                    ("FC", "Fotometro de Chama"),
                    ("ES", "Espectrofotometro"),
                    ("TI", "Titulacao"),
                    ("PH", "pHmetro"),
                ],
                max_length=2,
            ),
        ),
        migrations.AlterField(
            model_name="cliente",
            name="codigo",
            field=models.CharField(max_length=50, unique=True, verbose_name="Codigo"),
        ),
        migrations.AlterField(
            model_name="laudo",
            name="data_emissao",
            field=models.DateField(default=datetime.date.today, verbose_name="Data de Entrada"),
        ),
        migrations.AddConstraint(
            model_name="leituraequipamento",
            constraint=models.UniqueConstraint(
                fields=("analise", "bateria"),
                name="unique_leitura_por_analise_bateria",
            ),
        ),
    ]

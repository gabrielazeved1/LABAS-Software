# Generated manually — Sprint 7: Refatoração 1:N (Laudo → N Análises)
# Passo 1/3: Cria model Laudo e adiciona campos nullable em AnaliseSolo.

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0015_alter_analisesolo_options_and_more"),
    ]

    operations = [
        # 1. Cria o model Laudo (cabeçalho do documento)
        migrations.CreateModel(
            name="Laudo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "codigo_laudo",
                    models.CharField(
                        editable=False,
                        max_length=20,
                        unique=True,
                        verbose_name="Código do Laudo",
                    ),
                ),
                (
                    "data_emissao",
                    models.DateField(
                        default=django.utils.timezone.now,
                        verbose_name="Data de Emissão",
                    ),
                ),
                (
                    "observacoes",
                    models.TextField(blank=True, null=True, verbose_name="Observações"),
                ),
                (
                    "cliente",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="laudos",
                        to="database.cliente",
                    ),
                ),
            ],
            options={
                "verbose_name": "Laudo",
                "verbose_name_plural": "Laudos",
            },
        ),
        # 2. Adiciona FK nullable laudo em AnaliseSolo (nullable p/ migration de dados)
        migrations.AddField(
            model_name="analisesolo",
            name="laudo",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="analises",
                to="database.laudo",
            ),
        ),
        # 3. Adiciona campo ativo
        migrations.AddField(
            model_name="analisesolo",
            name="ativo",
            field=models.BooleanField(default=True, verbose_name="Ativo"),
        ),
        # 4. Adiciona campo referencia (coluna exibida no PDF)
        migrations.AddField(
            model_name="analisesolo",
            name="referencia",
            field=models.CharField(
                blank=True,
                max_length=100,
                null=True,
                verbose_name="Referência Cliente",
            ),
        ),
        # 5. Remove unique=True do n_lab (unicidade agora é por laudo via unique_together)
        migrations.AlterField(
            model_name="analisesolo",
            name="n_lab",
            field=models.CharField(max_length=50, verbose_name="N Lab"),
        ),
    ]

# Generated manually — Sprint 7: Refatoração 1:N (Laudo → N Análises)
# Passo 3/3: Torna laudo NOT NULL, remove cliente FK, adiciona unique_together.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0017_data_link_analises_laudos"),
    ]

    operations = [
        # 1. Torna laudo FK NOT NULL (todos os registros já foram vinculados em 0017)
        migrations.AlterField(
            model_name="analisesolo",
            name="laudo",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="analises",
                to="database.laudo",
            ),
        ),
        # 2. Remove FK cliente de AnaliseSolo (cliente agora está em Laudo)
        migrations.RemoveField(
            model_name="analisesolo",
            name="cliente",
        ),
        # 3. Aplica unicidade de n_lab no escopo do laudo
        migrations.AlterUniqueTogether(
            name="analisesolo",
            unique_together={("laudo", "n_lab")},
        ),
        # 4. Atualiza verbose_name do model
        migrations.AlterModelOptions(
            name="analisesolo",
            options={
                "verbose_name": "Analise de Solo",
                "verbose_name_plural": "Analises de Solo",
            },
        ),
    ]

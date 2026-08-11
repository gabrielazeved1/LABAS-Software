from django.db import migrations


def remover_leituras_duplicadas(apps, schema_editor):
    """
    Para cada par (analise, bateria) com mais de uma leitura, mantém apenas
    a mais recente (maior id) e remove as demais.
    """
    LeituraEquipamento = apps.get_model("database", "LeituraEquipamento")

    from django.db.models import Count, Max

    grupos = (
        LeituraEquipamento.objects
        .values("analise_id", "bateria_id")
        .annotate(total=Count("id"), ultimo_id=Max("id"))
        .filter(total__gt=1)
    )

    for grupo in grupos:
        LeituraEquipamento.objects.filter(
            analise_id=grupo["analise_id"],
            bateria_id=grupo["bateria_id"],
        ).exclude(id=grupo["ultimo_id"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0021_analise_n_lab_unique_global"),
    ]

    operations = [
        migrations.RunPython(
            remover_leituras_duplicadas,
            migrations.RunPython.noop,
        ),
    ]

# Generated manually — Sprint 7: Refatoração 1:N (Laudo → N Análises)
# Passo 2/3: Data migration — cria Laudos stub por cliente e vincula AnaliseSolo.

from datetime import date

from django.db import migrations


def criar_laudos_stub(apps, schema_editor):
    """
    Para cada Cliente que possui AnaliseSolo, cria um único Laudo stub
    e vincula todas as suas análises a esse laudo.
    """
    AnaliseSolo = apps.get_model("database", "AnaliseSolo")
    Laudo = apps.get_model("database", "Laudo")

    ano = date.today().year
    cliente_ids = (
        AnaliseSolo.objects.values_list("cliente_id", flat=True)
        .distinct()
        .order_by("cliente_id")
    )

    for cliente_id in cliente_ids:
        count = Laudo.objects.filter(codigo_laudo__startswith=f"L-{ano}/").count()
        laudo = Laudo.objects.create(
            codigo_laudo=f"L-{ano}/{count + 1}",
            cliente_id=cliente_id,
            data_emissao=date.today(),
        )
        AnaliseSolo.objects.filter(cliente_id=cliente_id).update(laudo=laudo)


def desfazer_laudos_stub(apps, schema_editor):
    """Reverte: desvincula AnaliseSolo e remove laudos stub."""
    AnaliseSolo = apps.get_model("database", "AnaliseSolo")
    Laudo = apps.get_model("database", "Laudo")
    AnaliseSolo.objects.all().update(laudo=None)
    Laudo.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0016_add_laudo_model"),
    ]

    operations = [
        migrations.RunPython(criar_laudos_stub, desfazer_laudos_stub),
    ]

from decimal import Decimal
from src.application.equipamentos.phmetro import LeitorPHmetro

print("==================================================")
print("TESTE DO pHMETRO (LEITURA DIRETA E VALIDAÇÃO)")
print("==================================================")

leitor = LeitorPHmetro()

# Simulando o técnico digitando os valores do visor
leitura_agua = Decimal("6.25")
leitura_cacl2 = Decimal("5.50")
leitura_kcl = Decimal("5.10")

try:
    resultados = leitor.registrar_leituras(
        ph_agua=leitura_agua, ph_cacl2=leitura_cacl2, ph_kcl=leitura_kcl
    )

    print("Leituras Registradas com Sucesso:")
    print(f"-> pH (H2O):   {resultados.get('ph_agua')}")
    print(f"-> pH (CaCl2): {resultados.get('ph_cacl2')}")
    print(f"-> pH (KCl):   {resultados.get('ph_kcl')}")

except ValueError as e:
    print(f"Falha na Validação: {e}")

print("\n==================================================")
print("TESTANDO A TRAVA DE SEGURANÇA (Erro de Digitação)")
print("==================================================")

# Simulando o técnico esbarrando no teclado e digitando "65.2" em vez de "6.52"
leitura_errada = Decimal("65.2")

try:
    leitor.registrar_leituras(ph_agua=leitura_errada)
except ValueError as e:
    print(f"O sistema bloqueou o erro com sucesso: \n   {e}")

print("==================================================")

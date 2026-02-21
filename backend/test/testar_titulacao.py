from decimal import Decimal
from src.application.equipamentos.titulacao import CalculadoraTitulacao

print("==================================================")
print("🧪 TESTE DE TITULAÇÃO: ALUMÍNIO E ACIDEZ POTENCIAL")
print("==================================================")

calculadora = CalculadoraTitulacao()

# ---------------------------------------------------------
# 1. Testando o Alumínio (Al3+) - Imagem 1
# ---------------------------------------------------------
print("\n---> 1. TESTANDO ALUMÍNIO (Al3+)")
branco_al = Decimal("0.00")  # Conforme sua imagem do Al
amostras_al = [
    ("Padrão A", Decimal("0.41")),
    ("P. Labas A", Decimal("0.39")),
    ("2025/13", Decimal("0.00")),  # Testando a trava de zero
]

print(f"Branco Inserido: {branco_al} cmolc/dm³")
for nome, leitura in amostras_al:
    resultado = calculadora.calcular_aluminio(
        leitura_amostra=leitura, leitura_branco=branco_al
    )
    print(f"Amostra {nome}: Lido = {leitura} -> Resultado Final = {resultado}")

# ---------------------------------------------------------
# 2. Testando Acidez Potencial (H+Al) - Imagem 2
# ---------------------------------------------------------
print("\n---> 2. TESTANDO ACIDEZ POTENCIAL (H+Al)")
branco_hal = Decimal("0.10")  # Valor simulado para forçar a subtração
amostras_hal = [
    ("Padrão A", Decimal("2.80")),
    ("P. Labas B", Decimal("1.47")),
    ("2025/14", Decimal("0.49")),
]

print(f"Branco Simulado Inserido: {branco_hal} cmolc/dm³")
for nome, leitura in amostras_hal:
    resultado = calculadora.calcular_acidez_potencial(
        leitura_amostra=leitura, leitura_branco=branco_hal
    )
    print(
        f"Amostra {nome}: Lido = {leitura} -> Fórmula ({leitura} - {branco_hal}) = {resultado}"
    )

print("\n==================================================")
print("✅ MÓDULO DE TITULAÇÃO CONCLUÍDO COM SUCESSO!")

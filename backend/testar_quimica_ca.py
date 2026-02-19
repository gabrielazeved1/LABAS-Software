from decimal import Decimal, getcontext
from src.application.equipamentos.core_matematico import CurvaRegressaoLinear
from src.application.equipamentos.absorcao_atomica import CalculadoraAbsorcaoAtomica

# Aumenta a precisão interna do Decimal para evitar qualquer perda nas divisões
getcontext().prec = 10

print("🧪 A INICIAR TESTE DA PLANILHA DE CÁLCIO (Ca_KCl)...\n")

# 1. Dados da Tabela Azul (Extraídos da sua imagem)
valores_x = [
    Decimal("0"),
    Decimal("1"),
    Decimal("2"),
    Decimal("4"),
    Decimal("8"),
    Decimal("16"),
]
valores_y = [
    Decimal("-0.0002"),
    Decimal("0.0639"),
    Decimal("0.1086"),
    Decimal("0.1959"),
    Decimal("0.3621"),
    Decimal("0.663"),
]

# 2. O Motor Matemático gera a Curva
curva = CurvaRegressaoLinear(valores_x, valores_y)

print("📊 RESULTADOS DA REGRESSÃO LINEAR (Comparando com o Excel):")
print(
    f"Inclinação (M17 no Excel): {curva.a.quantize(Decimal('0.00001'))} (Esperado: ~0.04076)"
)
print(
    f"Intercepto (M18 no Excel): {curva.b.quantize(Decimal('0.00001'))} (Esperado: ~0.02162)\n"
)

# 3. Teste da Amostra (P. Labas B ou 2025/19)
maquina = CalculadoraAbsorcaoAtomica()

# Parâmetros que você pediu para testar
absorvancia_lida = Decimal("0.1731")  # F12
diluicao = Decimal("10.00")  # D12 (ou E12 dependendo da coluna exata)
vol_extrator = Decimal("50.00")  # E12
vol_solo = Decimal("0.005")  # C12

# 4. Cálculo final do Cálcio
resultado_ca = maquina.calcular_ca_disponivel(
    leitura_absorvancia=absorvancia_lida,
    coeficiente_angular_a=curva.a,
    coeficiente_linear_b=curva.b,
    volume_extrator_ml=vol_extrator,
    fator_diluicao=diluicao,
    volume_solo_cm3=vol_solo,
)

print("🌱 RESULTADO AGRONÔMICO:")
print(f"Absorbância Lida: {absorvancia_lida}")
print(f"Ca-disponível (cmol_c/dm³): {resultado_ca}")
print("\n✅ Teste concluído!")

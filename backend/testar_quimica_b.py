from decimal import Decimal, getcontext
from src.application.equipamentos.core_matematico import CurvaRegressaoLinear
from src.application.equipamentos.espectrofotometro import CalculadoraEspectrofotometro

getcontext().prec = 10

print("🧪 TESTE DO BORO (B) - ESPECTROFOTÔMETRO\n")

# 1. Dados da Curva de Calibração (Boro)
valores_x = [
    Decimal("0"),
    Decimal("0.2"),
    Decimal("0.4"),
    Decimal("0.6"),
    Decimal("0.8"),
    Decimal("1"),
]
valores_y = [
    Decimal("0.000013"),
    Decimal("0.161"),
    Decimal("0.312917"),
    Decimal("0.41602"),
    Decimal("0.555112"),
    Decimal("0.667097"),
]

curva_b = CurvaRegressaoLinear(valores_x, valores_y)

inclinacao_b = curva_b.a  # N16 no Excel (O Excel chama de 'b')
intercepto_a = curva_b.b  # N17 no Excel (O Excel chama de 'a')

print("==================================================")
print("📈 LAUDO DE CALIBRAÇÃO (EQUAÇÃO DA RETA)")
print("==================================================")
# Ajusta o sinal visualmente para a equação ficar correta (ex: + 0.02 ou - 0.02)
sinal = "+" if intercepto_a >= 0 else "-"
equacao = f"y = {inclinacao_b.quantize(Decimal('0.000001'))}x {sinal} {abs(intercepto_a).quantize(Decimal('0.000001'))}"

print(f"Equação Gerada: {equacao}")
print(f"-> 'b' (Inclinação / N16): {inclinacao_b.quantize(Decimal('0.000001'))}")
print(f"-> 'a' (Intercepto / N17): {intercepto_a.quantize(Decimal('0.000001'))}\n")

print("==================================================")
print("🔍 TESTE DE CÁLCULO DA AMOSTRA (Com Logaritmo)")
print("==================================================")
maquina = CalculadoraEspectrofotometro()

# Lembrete: A fórmula do Excel para o Boro "=((G8)/N$16)..." IGNORA o intercepto (N17).
# Ela divide a Absorbância direto pela Inclinação (N16).
transmitancia_lida = Decimal("94.10")  # F8: O aparelho leu 45.5% (Transmitância)
vol_extrator = Decimal("20")
diluicao = Decimal("1.5")
vol_solo = Decimal("0.01")

resultado_b = maquina.calcular_b_disponivel(
    leitura_transmitancia=transmitancia_lida,
    coeficiente_angular_a=inclinacao_b,
    volume_extrator_ml=vol_extrator,
    fator_diluicao=diluicao,
    volume_solo_cm3=vol_solo,
)

abs_calculada = Decimal("2") - transmitancia_lida.log10()

print(f"1. Transmitância Lida: {transmitancia_lida}%")
print(f"2. Conversão para Absorbância: {abs_calculada.quantize(Decimal('0.0001'))}")
print(f"3. Resultado B-disponível: {resultado_b} mg/dm³")
print("==================================================")

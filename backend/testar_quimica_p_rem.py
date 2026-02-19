from decimal import Decimal, getcontext
from src.application.equipamentos.core_matematico import CurvaRegressaoLinear
from src.application.equipamentos.espectrofotometro import CalculadoraEspectrofotometro

getcontext().prec = 10

# 1. Dados da Curva de Calibração (P-rem)
valores_x = [
    Decimal("0"),
    Decimal("0.3"),
    Decimal("0.6"),
    Decimal("0.9"),
    Decimal("1.2"),
    Decimal("1.5"),
]
valores_y = [
    Decimal("0"),
    Decimal("0.099"),
    Decimal("0.206"),
    Decimal("0.326"),
    Decimal("0.434"),
    Decimal("0.543"),
]

curva_p_rem = CurvaRegressaoLinear(valores_x, valores_y)

inclinacao_p_rem = curva_p_rem.a  # N16
intercepto_a = curva_p_rem.b  # N17

print("==================================================")
print("📈 LAUDO DE CALIBRAÇÃO (EQUAÇÃO DA RETA) - P-rem")
print("==================================================")
sinal = "+" if intercepto_a >= 0 else "-"
equacao = f"y = {inclinacao_p_rem.quantize(Decimal('0.0001'))}x {sinal} {abs(intercepto_a).quantize(Decimal('0.0001'))}"

print(f"Equação Gerada: {equacao}")
print(
    f"-> 'b' (Inclinação): {inclinacao_p_rem.quantize(Decimal('0.000001'))} (Esperado: 0.365714)"
)
print(
    f"-> 'a' (Intercepto): {intercepto_a.quantize(Decimal('0.000001'))} (Esperado: -0.006286)\n"
)

print("==================================================")
print("🔍 TESTE DA AMOSTRA (Transmitância = 51.26%)")
print("==================================================")
maquina = CalculadoraEspectrofotometro()

# Parâmetros para o teste (Transmitância pedida e assumindo E11 = 50)
transmitancia_lida = Decimal("61.04")
fator_e = Decimal("50")  # Valor da Coluna E (Diluição)

resultado_p_rem = maquina.calcular_p_rem(
    leitura_transmitancia=transmitancia_lida,
    coeficiente_angular_a=inclinacao_p_rem,
    coeficiente_linear_b=intercepto_a,
    fator_coluna_e=fator_e,
)

# Prova real
abs_calculada = Decimal("2") - transmitancia_lida.log10()

print(f"1. Transmitância Lida: {transmitancia_lida}%")
print(f"2. Absorbância Calculada: {abs_calculada.quantize(Decimal('0.00001'))}")
print(f"3. Valor do multiplicador (Coluna E): {fator_e}")
print(f"4. Resultado Final P-rem: {resultado_p_rem} mg/L")
print("==================================================")
print("✅ ESPECTROFOTÔMETRO AGORA SIM, 100% FINALIZADO!")

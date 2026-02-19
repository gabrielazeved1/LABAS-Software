from decimal import Decimal, getcontext
from src.application.equipamentos.core_matematico import CurvaRegressaoLinear
from src.application.equipamentos.espectrofotometro import CalculadoraEspectrofotometro

getcontext().prec = 10

# 1. Dados da Curva de Calibração (Enxofre)
valores_x = [
    Decimal("0"),
    Decimal("0.3"),
    Decimal("0.6"),
    Decimal("0.9"),
    Decimal("1.2"),
    Decimal("2"),
    Decimal("4"),
    Decimal("6"),
    Decimal("8"),
    Decimal("10"),
]
valores_y = [
    Decimal("0.0000738"),
    Decimal("0.014012"),
    Decimal("0.031018"),
    Decimal("0.032092"),
    Decimal("0.041622"),
    Decimal("0.053062"),
    Decimal("0.070081"),
    Decimal("0.095479"),
    Decimal("0.126656"),
    Decimal("0.175829"),
]

curva_s = CurvaRegressaoLinear(valores_x, valores_y)

inclinacao_s = curva_s.a
intercepto_a = curva_s.b

print("==================================================")
print("📈 LAUDO DE CALIBRAÇÃO (EQUAÇÃO DA RETA) - ENXOFRE")
print("==================================================")
sinal = "+" if intercepto_a >= 0 else "-"
equacao = f"y = {inclinacao_s.quantize(Decimal('0.0001'))}x {sinal} {abs(intercepto_a).quantize(Decimal('0.0001'))}"

print(f"Equação Gerada: {equacao}")
print(f"-> 'b' (Inclinação): {inclinacao_s.quantize(Decimal('0.000001'))}")
print(f"-> 'a' (Intercepto): {intercepto_a.quantize(Decimal('0.000001'))}\n")

print("==================================================")
print("🔍 TESTE DA AMOSTRA: REGRA OFICIAL (COM INTERCEPTO)")
print("==================================================")
maquina = CalculadoraEspectrofotometro()

transmitancia_lida = Decimal("85.50")
vol_extrator = Decimal("25.00")
diluicao = Decimal("1.15")
vol_solo = Decimal("0.010")

resultado_s = maquina.calcular_s_disponivel(
    leitura_transmitancia=transmitancia_lida,
    coeficiente_angular_a=inclinacao_s,
    coeficiente_linear_b=intercepto_a,  # PASSANDO O INTERCEPTO AGORA!
    volume_extrator_ml=vol_extrator,
    fator_diluicao=diluicao,
    volume_solo_cm3=vol_solo,
)

abs_calculada = Decimal("2") - transmitancia_lida.log10()

print(f"Transmitância Lida: {transmitancia_lida}%")
print(f"Absorbância Calculada: {abs_calculada.quantize(Decimal('0.00001'))}")
print(f"Resultado Final S-disponível: {resultado_s} mg/dm³")
print("✅ Teste Finalizado e alinhado com a Jéssica!")

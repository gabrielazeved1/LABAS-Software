from decimal import Decimal, getcontext
from src.application.equipamentos.core_matematico import CurvaRegressaoLinear
from src.application.equipamentos.espectrofotometro import CalculadoraEspectrofotometro

getcontext().prec = 10

# 1. Dados da Curva de Calibração (Extraídos da sua imagem de P)
valores_x = [
    Decimal("0"),
    Decimal("0.4"),
    Decimal("0.8"),
    Decimal("1.2"),
    Decimal("1.6"),
    Decimal("2"),
]
valores_y = [
    Decimal("0"),
    Decimal("0.291579"),
    Decimal("0.447332"),
    Decimal("0.638272"),
    Decimal("0.90309"),
    Decimal("1.154902"),
]

curva_p = CurvaRegressaoLinear(valores_x, valores_y)

inclinacao_p = curva_p.a
intercepto_a = curva_p.b

print("==================================================")
print("LAUDO DE CALIBRAÇÃO (EQUAÇÃO DA RETA) - FÓSFORO")
print("==================================================")
sinal = "+" if intercepto_a >= 0 else "-"
equacao = f"y = {inclinacao_p.quantize(Decimal('0.0001'))}x {sinal} {abs(intercepto_a).quantize(Decimal('0.0001'))}"

print(f"Equação Gerada: {equacao}")
print(
    f"-> 'b' (Inclinação): {inclinacao_p.quantize(Decimal('0.000001'))} (Esperado: 0.557142)"
)
print(
    f"-> 'a' (Intercepto): {intercepto_a.quantize(Decimal('0.000001'))} (Esperado: 0.015388)\n"
)


maquina = CalculadoraEspectrofotometro()

# Parâmetros solicitados para o teste
transmitancia_lida = Decimal("75.30")
vol_extrator = Decimal("50.00")
diluicao = Decimal("2")
vol_solo = Decimal("0.005")

resultado_p = maquina.calcular_p_mehlich_disponivel(
    leitura_transmitancia=transmitancia_lida,
    coeficiente_angular_a=inclinacao_p,
    coeficiente_linear_b=intercepto_a,
    volume_extrator_ml=vol_extrator,
    fator_diluicao=diluicao,
    volume_solo_cm3=vol_solo,
)

# Prova real do cálculo
abs_calculada = Decimal("2") - transmitancia_lida.log10()

print(f"1. Transmitância Lida: {transmitancia_lida}%")
print(f"2. Absorbância Calculada: {abs_calculada.quantize(Decimal('0.000001'))}")
print(f"3. Resultado Final P-disponível: {resultado_p} mg/dm³")
print("==================================================")
print("ESPECTROFOTÔMETRO CONCLUÍDO COM SUCESSO!")

from decimal import Decimal, getcontext
from src.application.equipamentos.core_matematico import CurvaRegressaoLinear
from src.application.equipamentos.espectrofotometro import CalculadoraEspectrofotometro

getcontext().prec = 10

# 1. Dados da Curva de Calibração (P-Resina)
valores_x = [
    Decimal("0"),
    Decimal("0.8"),
    Decimal("1.6"),
    Decimal("2.4"),
    Decimal("3.2"),
    Decimal("4"),
    Decimal("4.8"),
    Decimal("5.6"),
    Decimal("6.4"),
]
valores_y = [
    Decimal("0.004"),
    Decimal("0.031"),
    Decimal("0.059"),
    Decimal("0.085"),
    Decimal("0.116"),
    Decimal("0.140"),
    Decimal("0.169"),
    Decimal("0.212"),
    Decimal("0.235"),
]

curva_p_resina = CurvaRegressaoLinear(valores_x, valores_y)

inclinacao_p = curva_p_resina.a  # N19
intercepto_a = curva_p_resina.b  # N20

print("==================================================")
print("LAUDO DE CALIBRAÇÃO (EQUAÇÃO DA RETA) - P-RESINA")
print("==================================================")
sinal = "+" if intercepto_a >= 0 else "-"
equacao = f"y = {inclinacao_p.quantize(Decimal('0.0001'))}x {sinal} {abs(intercepto_a).quantize(Decimal('0.0001'))}"

print(f"Equação Gerada: {equacao}")
print(
    f"-> 'b' (Inclinação): {inclinacao_p.quantize(Decimal('0.000001'))} (Esperado: 0.036276)"
)
print(
    f"-> 'a' (Intercepto): {intercepto_a.quantize(Decimal('0.000001'))} (Esperado: 0.000646)\n"
)

print("==================================================")
print("TESTE DAS AMOSTRAS (Transmitâncias: 50% e 90%)")
print("==================================================")
maquina = CalculadoraEspectrofotometro()

vol_extrator = Decimal("50.00")
diluicao = Decimal("1")
vol_solo = Decimal("0.0025")

transmitancias_para_testar = [Decimal("50"), Decimal("90")]

for trans_lida in transmitancias_para_testar:
    resultado = maquina.calcular_p_resina_disponivel(
        leitura_transmitancia=trans_lida,
        coeficiente_angular_a=inclinacao_p,
        coeficiente_linear_b=intercepto_a,
        volume_extrator_ml=vol_extrator,
        fator_diluicao=diluicao,
        volume_solo_cm3=vol_solo,
    )

    abs_calculada = Decimal("2") - trans_lida.log10()

    print(f"🔹 Teste com Transmitância: {trans_lida}%")
    print(f"   Absorbância Calculada: {abs_calculada.quantize(Decimal('0.000001'))}")
    print(f"   Resultado Final P-Resina: {resultado} mg/dm³\n")

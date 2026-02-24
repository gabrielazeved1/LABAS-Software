from decimal import Decimal, getcontext
from src.application.equipamentos.core_matematico import CurvaRegressaoLinear
from src.application.equipamentos.fotometro_chama import CalculadoraFotometroChama

getcontext().prec = 10

# 1. Dados da Curva de Calibração (Sódio - Na) baseados na TABELA
valores_x = [
    Decimal("0"),
    Decimal("20"),
    Decimal("40"),
    Decimal("60"),
    Decimal("80"),
    Decimal("100"),
]
valores_y = [
    Decimal("0"),
    Decimal("18"),
    Decimal("39"),
    Decimal("57"),
    Decimal("79"),
    Decimal("100"),
]

curva_na = CurvaRegressaoLinear(valores_x, valores_y)

inclinacao_na = curva_na.a  # L16
intercepto_a = curva_na.b  # L17

print("==================================================")
print("LAUDO DE CALIBRAÇÃO (EQUAÇÃO DA RETA) - SÓDIO")
print("==================================================")
sinal = "+" if intercepto_a >= 0 else "-"
equacao = f"y = {inclinacao_na.quantize(Decimal('0.0001'))}x {sinal} {abs(intercepto_a).quantize(Decimal('0.0001'))}"

print(f"Equação REAL (Não a do gráfico com bug): {equacao}")
print(
    f"-> 'b' (Inclinação): {inclinacao_na.quantize(Decimal('0.000001'))} (Esperado: 1.001429)"
)
print(
    f"-> 'a' (Intercepto): {intercepto_a.quantize(Decimal('0.000001'))} (Esperado: -1.238095)\n"
)

print("==================================================")
print("TESTE DAS AMOSTRAS (5 Valores de Emissão)")
print("==================================================")
maquina = CalculadoraFotometroChama()

vol_extrator = Decimal("50.00")
diluicao = Decimal("1")
vol_solo = Decimal("0.005")

# 5 valores simulados de Emissão (Baixo a Alto)
emissoes_para_testar = [
    Decimal("10"),
    Decimal("25"),
    Decimal("50"),
    Decimal("75"),
    Decimal("95"),
]

for emissao_lida in emissoes_para_testar:
    resultado = maquina.calcular_na_disponivel(
        leitura_emissao=emissao_lida,
        coeficiente_angular_a=inclinacao_na,
        coeficiente_linear_b=intercepto_a,
        volume_extrator_ml=vol_extrator,
        fator_diluicao=diluicao,
        volume_solo_cm3=vol_solo,
    )

    print(f"Emissão Lida: {emissao_lida} u.a. -> Sódio Disponível: {resultado} mg/dm³")

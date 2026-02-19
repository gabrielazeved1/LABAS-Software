from decimal import Decimal, getcontext
from src.application.equipamentos.core_matematico import CurvaRegressaoLinear
from src.application.equipamentos.absorcao_atomica import CalculadoraAbsorcaoAtomica

getcontext().prec = 10

print("🧪 A INICIAR TESTE DA PLANILHA DE FERRO (Fe)...\n")

# 1. Dados Exatos da Curva de Calibração do Fe (Da imagem enviada)
valores_x = [
    Decimal("0"),
    Decimal("3"),
    Decimal("6"),
    Decimal("9"),
    Decimal("12"),
    Decimal("15"),
]
valores_y = [
    Decimal("-0.0003"),
    Decimal("0.0226"),
    Decimal("0.0456"),
    Decimal("0.0657"),
    Decimal("0.0859"),
    Decimal("0.1052"),
]

# O Motor gera a Reta de Regressão Linear a partir dos padrões
curva_fe = CurvaRegressaoLinear(valores_x, valores_y)

inclinacao = curva_fe.a  # L16 no Excel
intercepto = curva_fe.b  # L17 no Excel

print("==================================================")
print("📈 EQUAÇÃO DE PRIMEIRO GRAU CRIADA (FERRO)")
print("==================================================")
print(
    f"y = {inclinacao.quantize(Decimal('0.0000001'))}x + {intercepto.quantize(Decimal('0.0000001'))}"
)
print(
    f"Inclinação (L16): {inclinacao.quantize(Decimal('0.000001'))} (Esperado pelo Excel: ~0.007024)"
)
print(
    f"Intercepto (L17): {intercepto.quantize(Decimal('0.000001'))} (Esperado pelo Excel: ~0.001438)\n"
)

print("==================================================")
print("🔍 TESTE DE CÁLCULO DE AMOSTRA")
print("==================================================")
maquina = CalculadoraAbsorcaoAtomica()

# Parâmetros reais fixos da rotina do laboratório
emissao_teste = Decimal("0.0231")  # Exemplo de leitura de uma amostra
vol_extrator = Decimal("50")
diluicao = Decimal("1")
vol_solo = Decimal("0.005")

resultado_fe = maquina.calcular_fe_disponivel(
    leitura_emissao=emissao_teste,
    coeficiente_angular_a=inclinacao,
    coeficiente_linear_b=intercepto,
    volume_extrator_ml=vol_extrator,
    fator_diluicao=diluicao,
    volume_solo_cm3=vol_solo,
)

print(f"Emissão Lida pelo Aparelho: {emissao_teste}")
print(f"Resultado Fe-disponível: {resultado_fe} mg/dm³")
print("✅ Teste finalizado.")

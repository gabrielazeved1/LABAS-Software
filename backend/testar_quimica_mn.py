from decimal import Decimal, getcontext
from src.application.equipamentos.core_matematico import CurvaRegressaoLinear
from src.application.equipamentos.absorcao_atomica import CalculadoraAbsorcaoAtomica

getcontext().prec = 10

print("🧪 A INICIAR TESTE DA PLANILHA DE MANGANÊS (Mn)...\n")

# 1. Dados Exatos da Curva de Calibração do Mn (Da imagem enviada)
valores_x = [
    Decimal("0"),
    Decimal("1"),
    Decimal("2"),
    Decimal("3"),
    Decimal("4"),
    Decimal("5"),
]
valores_y = [
    Decimal("-0.0003"),
    Decimal("0.0182"),
    Decimal("0.0369"),
    Decimal("0.0550"),
    Decimal("0.0722"),
    Decimal("0.0898"),
]

# O Motor gera a Reta de Regressão Linear a partir dos padrões
curva_mn = CurvaRegressaoLinear(valores_x, valores_y)

inclinacao = curva_mn.a  # L16 no Excel
intercepto = curva_mn.b  # L17 no Excel

print("==================================================")
print("📈 EQUAÇÃO DE PRIMEIRO GRAU CRIADA (MANGANÊS)")
print("==================================================")
print(
    f"y = {inclinacao.quantize(Decimal('0.0000001'))}x + {intercepto.quantize(Decimal('0.0000001'))}"
)
print(
    f"Inclinação (L16): {inclinacao.quantize(Decimal('0.000001'))} (Esperado na imagem: ~0.018017)"
)
print(
    f"Intercepto (L17): {intercepto.quantize(Decimal('0.000001'))} (Esperado na imagem: ~0.000257)\n"
)

print("==================================================")
print("🔍 TESTE DE CÁLCULO DE AMOSTRA")
print("==================================================")
maquina = CalculadoraAbsorcaoAtomica()

# Parâmetros reais fixos da rotina do laboratório
emissao_teste = Decimal("0.032")  # Simulando uma leitura aleatória do equipamento
vol_extrator = Decimal("50")
diluicao = Decimal("1")
vol_solo = Decimal("0.005")

resultado_mn = maquina.calcular_mn_disponivel(
    leitura_emissao=emissao_teste,
    coeficiente_angular_a=inclinacao,
    coeficiente_linear_b=intercepto,
    volume_extrator_ml=vol_extrator,
    fator_diluicao=diluicao,
    volume_solo_cm3=vol_solo,
)

print(f"Emissão Lida pelo Aparelho: {emissao_teste}")
print(f"Resultado Mn-disponível: {resultado_mn} mg/dm³")
print("✅ Teste finalizado com precisão máxima.")

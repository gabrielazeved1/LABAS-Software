from decimal import Decimal, getcontext
from src.application.equipamentos.core_matematico import CurvaRegressaoLinear
from src.application.equipamentos.absorcao_atomica import CalculadoraAbsorcaoAtomica

getcontext().prec = 10

print("🧪 A INICIAR TESTE DA PLANILHA DE ZINCO (Zn)...\n")

# 1. Dados Exatos da Curva de Calibração do Zn (Da imagem enviada)
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
    Decimal("0.0233"),
    Decimal("0.0463"),
    Decimal("0.0671"),
    Decimal("0.0883"),
    Decimal("0.1079"),
]

# O Motor gera a Reta de Regressão Linear
curva_zn = CurvaRegressaoLinear(valores_x, valores_y)

inclinacao = curva_zn.a  # L16 no Excel
intercepto = curva_zn.b  # L17 no Excel

print("==================================================")
print("📈 EQUAÇÃO DE PRIMEIRO GRAU CRIADA (ZINCO)")
print("==================================================")
print(
    f"y = {inclinacao.quantize(Decimal('0.0000001'))}x + {intercepto.quantize(Decimal('0.0000001'))}"
)
print(
    f"Inclinação (L16): {inclinacao.quantize(Decimal('0.000001'))} (Esperado na imagem: ~0.053950)"
)
print(
    f"Intercepto (L17): {intercepto.quantize(Decimal('0.000001'))} (Esperado na imagem: ~0.001533)\n"
)

print("==================================================")
print("🔍 TESTE DE CÁLCULO DE AMOSTRA")
print("==================================================")
maquina = CalculadoraAbsorcaoAtomica()

# Parâmetros reais fixos da rotina
emissao_teste = Decimal("0.05641")  # Exemplo de leitura do equipamento
vol_extrator = Decimal("50")
diluicao = Decimal("1")
vol_solo = Decimal("0.005")

resultado_zn = maquina.calcular_zn_disponivel(
    leitura_emissao=emissao_teste,
    coeficiente_angular_a=inclinacao,
    coeficiente_linear_b=intercepto,
    volume_extrator_ml=vol_extrator,
    fator_diluicao=diluicao,
    volume_solo_cm3=vol_solo,
)

print(f"Emissão Lida pelo Aparelho: {emissao_teste}")
print(f"Resultado Zn-disponível: {resultado_zn} mg/dm³")
print("✅ Módulo de Absorção Atômica CONCLUÍDO COM SUCESSO!")

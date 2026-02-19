from decimal import Decimal, getcontext
from src.application.equipamentos.core_matematico import CurvaRegressaoLinear
from src.application.equipamentos.absorcao_atomica import CalculadoraAbsorcaoAtomica

getcontext().prec = 10

print("🧪 A INICIAR TESTE DA PLANILHA DE COBRE (Cu)...\n")

# 1. Dados Exatos da Curva de Calibração do Cu (Extraídos da sua imagem)
valores_x = [
    Decimal("0"),
    Decimal("0.4"),
    Decimal("0.8"),
    Decimal("1.2"),
    Decimal("1.6"),
    Decimal("2.0"),
]
valores_y = [
    Decimal("0"),
    Decimal("0.005"),
    Decimal("0.0111"),
    Decimal("0.0169"),
    Decimal("0.0222"),
    Decimal("0.0282"),
]

# O Motor gera a Reta de Regressão Linear a partir dos padrões
curva_cu = CurvaRegressaoLinear(valores_x, valores_y)

inclinacao = curva_cu.a  # L16 no Excel
intercepto = curva_cu.b  # L17 no Excel

print("==================================================")
print("📈 EQUAÇÃO DE PRIMEIRO GRAU CRIADA (COBRE)")
print("==================================================")
# Ajustamos o sinal para ficar bonito caso o intercepto seja negativo
sinal = "+" if intercepto >= 0 else "-"
print(
    f"y = {inclinacao.quantize(Decimal('0.0000001'))}x {sinal} {abs(intercepto).quantize(Decimal('0.0000001'))}"
)
print(
    f"Inclinação (L16): {inclinacao.quantize(Decimal('0.000001'))} (Esperado pelo Excel: ~0.014171)"
)
print(
    f"Intercepto (L17): {intercepto.quantize(Decimal('0.000001'))} (Esperado pelo Excel: ~-0.00027)\n"
)

print("==================================================")
print("🔍 TESTE DA AMOSTRA 2025/14 (O Fantasma do '0,00')")
print("==================================================")
maquina = CalculadoraAbsorcaoAtomica()

# Parâmetros reais.
# O Excel mostra "0,00", mas calculando a engenharia reversa para dar 1,32,
# a máquina leu aproximadamente 0.0013 de absorbância.
emissao_crua = Decimal("0.0061")
vol_extrator = Decimal("50")
diluicao = Decimal("1")
vol_solo = Decimal("0.005")

resultado_cu = maquina.calcular_cu_disponivel(
    leitura_emissao=emissao_crua,
    coeficiente_angular_a=inclinacao,
    coeficiente_linear_b=intercepto,
    volume_extrator_ml=vol_extrator,
    fator_diluicao=diluicao,
    volume_solo_cm3=vol_solo,
)

print(f"Emissão Real Lida pelo Aparelho: {emissao_crua}")
print(f"Resultado Cu-disponível: {resultado_cu} mg/dm³ (Esperado na Coluna G: 4.50)")
print("✅ Teste finalizado.")

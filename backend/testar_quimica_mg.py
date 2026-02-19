from decimal import Decimal, getcontext
from src.application.equipamentos.core_matematico import CurvaRegressaoLinear

getcontext().prec = 10

# Dados Exatos da Curva de Mg (Imagem)
valores_x = [
    Decimal("0"),
    Decimal("0.5"),
    Decimal("1"),
    Decimal("2"),
    Decimal("4"),
    Decimal("8"),
]
valores_y = [
    Decimal("0"),
    Decimal("0.0484"),
    Decimal("0.0831"),
    Decimal("0.1497"),
    Decimal("0.2652"),
    Decimal("0.4366"),
]

curva = CurvaRegressaoLinear(valores_x, valores_y)

inclinacao = curva.a  # M17 no seu Excel (que ele chama de 'b')
intercepto = curva.b  # M18 no seu Excel (que ele chama de 'a')

print("==================================================")
print("EQUACAO DE PRIMEIRO GRAU")
print("==================================================")
print(
    f"Equação: y = {inclinacao.quantize(Decimal('0.00001'))}x + {intercepto.quantize(Decimal('0.00001'))}"
)
print("Onde:")
print("y = Absorbância (Coluna F)")
print("x = Concentração em mg/L")
print(f"M17 (Multiplica o x) = {inclinacao.quantize(Decimal('0.0000001'))}")
print(f"M18 (Soma no final)  = {intercepto.quantize(Decimal('0.0000001'))}\n")

print("==================================================")
print("Abs = 0.0457")
print("==================================================")
abs_lida = Decimal("0.0457")
vol_extrator = Decimal("50")
diluicao = Decimal("10")


concentracao = (abs_lida - intercepto) / inclinacao


massa_total = concentracao * vol_extrator * diluicao / Decimal("1000")

print(" ---------- CENARIO 1: O que a tela do Excel mostra (V-solo = 0.01)----------")
resultado_tela = massa_total / Decimal("0.01") / Decimal("120")
print(f"Mg = {resultado_tela.quantize(Decimal('0.01'))} cmol_c/dm³\n")

print("-----------CENARIO 2: O Fantasma do Excel (V-solo = 0.005)--------")
resultado_oculto = massa_total / Decimal("0.005") / Decimal("120")
print(f"Mg = {resultado_oculto.quantize(Decimal('0.01'))} cmol_c/dm³")

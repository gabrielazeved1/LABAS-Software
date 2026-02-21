from decimal import Decimal, getcontext
from src.application.equipamentos.core_matematico import CurvaRegressaoLinear
from src.application.equipamentos.absorcao_atomica import CalculadoraAbsorcaoAtomica

getcontext().prec = 10

print("==================================================")
print("🧪 TESTE ABSORÇÃO ATÔMICA: COBRE (Cu)")
print("==================================================")

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

curva = CurvaRegressaoLinear(valores_x, valores_y)

sinal = "+" if curva.b >= 0 else "-"
print("📈 LAUDO DE CALIBRAÇÃO (EQUAÇÃO DA RETA):")
print(
    f"Equação Gerada: y = {curva.a.quantize(Decimal('0.0001'))}x {sinal} {abs(curva.b).quantize(Decimal('0.0001'))}"
)
print(f"-> 'b' (Inclinação): {curva.a.quantize(Decimal('0.000001'))}")
print(f"-> 'a' (Intercepto): {curva.b.quantize(Decimal('0.000001'))}\n")

maquina = CalculadoraAbsorcaoAtomica()
branco_do_dia = Decimal("-0.0005")

amostras = [
    {"nome": "Amostra 1", "bruta": Decimal("0.0016")},
    {"nome": "Amostra 2025/14", "bruta": Decimal("0.0011")},
]

print(f"Branco do Lote: {branco_do_dia}\n")

for amostra in amostras:
    resultado = maquina.calcular_cu_disponivel(
        leitura_bruta=amostra["bruta"],
        leitura_branco=branco_do_dia,
        coeficiente_angular_a=curva.a,
        coeficiente_linear_b=curva.b,
        volume_extrator_ml=Decimal("50"),
        fator_diluicao=Decimal("1"),
        volume_solo_cm3=Decimal("0.005"),
    )
    print(
        f"-> {amostra['nome']} | Bruta: {amostra['bruta']} | Corrigida: {amostra['bruta'] - branco_do_dia}"
    )
    print(f"   Resultado (Cu): {resultado} mg/dm³\n")

from decimal import Decimal, getcontext
from src.application.equipamentos.core_matematico import CurvaRegressaoLinear
from src.application.equipamentos.absorcao_atomica import CalculadoraAbsorcaoAtomica

getcontext().prec = 10

print("==================================================")
print("🧪 TESTE ABSORÇÃO ATÔMICA: MAGNÉSIO (Mg)")
print("==================================================")

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

sinal = "+" if curva.b >= 0 else "-"
print("📈 LAUDO DE CALIBRAÇÃO (EQUAÇÃO DA RETA):")
print(
    f"Equação Gerada: y = {curva.a.quantize(Decimal('0.0001'))}x {sinal} {abs(curva.b).quantize(Decimal('0.0001'))}"
)
print(f"-> 'b' (Inclinação): {curva.a.quantize(Decimal('0.000001'))}")
print(f"-> 'a' (Intercepto): {curva.b.quantize(Decimal('0.000001'))}\n")

maquina = CalculadoraAbsorcaoAtomica()
branco_do_dia = Decimal("0.0222")

amostras = [
    {"nome": "Amostra 1", "bruta": Decimal("0.0769")},
    {"nome": "Amostra 2", "bruta": Decimal("0.0679")},
]

print(f"Branco do Lote: {branco_do_dia}\n")

for amostra in amostras:
    resultado = maquina.calcular_mg_disponivel(
        leitura_bruta=amostra["bruta"],
        leitura_branco=branco_do_dia,
        coeficiente_angular_a=curva.a,
        coeficiente_linear_b=curva.b,
        volume_extrator_ml=Decimal("50"),
        fator_diluicao=Decimal("10"),
        volume_solo_cm3=Decimal("0.005"),
    )
    print(
        f"-> {amostra['nome']} | Bruta: {amostra['bruta']} | Corrigida: {amostra['bruta'] - branco_do_dia}"
    )
    print(f"   Resultado (Mg): {resultado} cmolc/dm³\n")

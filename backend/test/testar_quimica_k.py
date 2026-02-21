from decimal import Decimal, getcontext
from src.application.equipamentos.core_matematico import CurvaRegressaoLinear
from src.application.equipamentos.fotometro_chama import CalculadoraFotometroChama

getcontext().prec = 10

# 1. Dados da Curva de Calibração (Potássio - K)
valores_x = [
    Decimal("0"),
    Decimal("4"),
    Decimal("8"),
    Decimal("12"),
    Decimal("16"),
    Decimal("20"),
]
valores_y = [
    Decimal("0"),
    Decimal("18"),
    Decimal("48"),
    Decimal("62"),
    Decimal("82"),
    Decimal("100"),
]

curva_k = CurvaRegressaoLinear(valores_x, valores_y)

inclinacao_k = curva_k.a  # L16
intercepto_a = curva_k.b  # L17

print("==================================================")
print("📈 LAUDO DE CALIBRAÇÃO (EQUAÇÃO DA RETA) - POTÁSSIO")
print("==================================================")
sinal = "+" if intercepto_a >= 0 else "-"
equacao = f"y = {inclinacao_k.quantize(Decimal('0.0001'))}x {sinal} {abs(intercepto_a).quantize(Decimal('0.0001'))}"

print(f"Equação Gerada: {equacao}")
print(
    f"-> 'b' (Inclinação): {inclinacao_k.quantize(Decimal('0.000001'))} (Esperado: 5.042857)"
)
print(
    f"-> 'a' (Intercepto): {intercepto_a.quantize(Decimal('0.000001'))} (Esperado: 1.238095)\n"
)

print("==================================================")
print("🔍 TESTE DAS AMOSTRAS (Emissões: 2 e 48)")
print("==================================================")
maquina = CalculadoraFotometroChama()

vol_extrator = Decimal("50.00")
diluicao = Decimal("1")
vol_solo = Decimal("0.005")

emissoes_para_testar = [Decimal("2"), Decimal("48")]

for emissao_lida in emissoes_para_testar:
    resultado = maquina.calcular_k_disponivel(
        leitura_emissao=emissao_lida,
        coeficiente_angular_a=inclinacao_k,
        coeficiente_linear_b=intercepto_a,
        volume_extrator_ml=vol_extrator,
        fator_diluicao=diluicao,
        volume_solo_cm3=vol_solo,
    )

    print(f"🔹 Teste com Emissão Lida: {emissao_lida} u.a.")
    print(f"   Resultado Final K-disponível: {resultado} mg/dm³\n")

from decimal import Decimal, getcontext
from src.application.equipamentos.espectrofotometro import CalculadoraEspectrofotometro

getcontext().prec = 10

print("==================================================")
print("LAUDO DE CALIBRAÇÃO (EQUAÇÃO FIXA) - M.O.")
print("==================================================")
# Valores extraídos da fórmula fixa do Excel: =(Abs + 0.0136) / 0.0729
inclinacao_mo_fixa = Decimal("0.0729")
intercepto_mo_fixo = Decimal("-0.0136")

sinal = "+" if intercepto_mo_fixo >= 0 else "-"
equacao = f"y = {inclinacao_mo_fixa}x {sinal} {abs(intercepto_mo_fixo)}"

print(f"Equação Padrão do Laboratório: {equacao}")
print(f"-> 'b' (Inclinação fixa): {inclinacao_mo_fixa}")
print(f"-> 'a' (Intercepto fixo): {intercepto_mo_fixo}\n")


maquina = CalculadoraEspectrofotometro()

# Para a absorbância dar ~0.1043, a transmitância lida foi de 78.65%
transmitancia_lida = Decimal("72.8")

# O cálculo chama apenas a leitura, pois a regra de negócio já embute os valores de a e b
resultado_mo = maquina.calcular_mo_disponivel(leitura_transmitancia=transmitancia_lida)

# Replicando o passo a passo para a tela
abs_calculada = Decimal("2") - transmitancia_lida.log10()

print(f"1. Transmitância Lida (Coluna F): {transmitancia_lida}%")
print(f"2. Absorbância (Coluna L): {abs_calculada.quantize(Decimal('0.0001'))}")
print(
    f"3. Fórmula Aplicada: ({abs_calculada.quantize(Decimal('0.0001'))} + {abs(intercepto_mo_fixo)}) / {inclinacao_mo_fixa}"
)
print(f"4. Resultado MO (MOS dag/kg): {resultado_mo} ")
print("==================================================")
print("✅ Teste com equação impressa finalizado!")

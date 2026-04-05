import { useState, useCallback } from "react";
import {
  calibracaoService,
  type BateriaCalibracaoComPontos,
} from "../services/calibracaoService";
import { entradaLoteService } from "../services/entradaLoteService";
import { useSnackbar } from "./useSnackbar";
import { REQUER_VOLUMES } from "../config/calibracaoConstants";
import type { Equipamento, Elemento } from "../types/calibracao";
import type { LinhaBancada } from "../types/entradaLote";

const normalizeDecimalInput = (value: string) =>
  value.replace(/,/g, ".").trim();

export function useEntradaLote() {
  const { showSuccess, showError, showApiError } = useSnackbar();

  const [equipamento, setEquipamento] = useState<Equipamento | "">("");
  const [elemento, setElemento] = useState<Elemento | "">("");
  const [bateriaAtiva, setBateriaAtiva] =
    useState<BateriaCalibracaoComPontos | null>(null);
  const [linhas, setLinhas] = useState<LinhaBancada[]>([]);
  const [loadingAmostras, setLoadingAmostras] = useState(false);
  const [salvando, setSalvando] = useState<Record<string, boolean>>({});
  // Evita exibir alertas de bateria antes da primeira pesquisa
  const [jaFiltrou, setJaFiltrou] = useState(false);

  /** Carrega a bateria ativa e as amostras pendentes para os filtros selecionados. */
  const handleFiltrar = useCallback(async () => {
    if (!equipamento || !elemento) {
      showError("Selecione o equipamento e o elemento antes de carregar.");
      return;
    }

    setLoadingAmostras(true);
    setBateriaAtiva(null);
    setLinhas([]);
    setJaFiltrou(true);

    try {
      const [bateria, amostras] = await Promise.all([
        calibracaoService.buscarBateriaAtiva(equipamento, elemento),
        entradaLoteService.buscarAmostrasPendentes(equipamento, elemento),
      ]);

      setBateriaAtiva(bateria);

      setLinhas(
        amostras.map((a) => ({
          ...a,
          equipamento,
          elemento,
          leitura_bruta: "",
          fator_diluicao: "",
          resultado_preview: null,
          status: "pendente",
        })),
      );
    } catch {
      showError(
        "Erro ao carregar amostras. Verifique a conexão com o servidor.",
      );
    } finally {
      setLoadingAmostras(false);
    }
  }, [equipamento, elemento, showError]);

  /**
   * Chamado automaticamente pelo DataGrid ao confirmar a edição de uma célula.
   * O backend é a única fonte de verdade: o resultado calculado é lido da resposta
   * da API após o salvamento da LeituraEquipamento.
   */
  const handleProcessRowUpdate = useCallback(
    async (
      newRow: LinhaBancada,
      oldRow: LinhaBancada,
    ): Promise<LinhaBancada> => {
      if (!bateriaAtiva) return oldRow;
      if (
        bateriaAtiva.equipamento !== equipamento ||
        bateriaAtiva.elemento !== elemento
      ) {
        showError(
          "A curva ativa nao corresponde ao equipamento/elemento selecionado.",
        );
        return oldRow;
      }

      const leituraNum = parseFloat(
        normalizeDecimalInput(newRow.leitura_bruta),
      );
      // Leitura ainda vazia: preserva valores intermediários (ex: fd já preenchido)
      // sem chamar a API ainda.
      if (isNaN(leituraNum)) return newRow;

      const precisaFd = REQUER_VOLUMES.includes(bateriaAtiva.equipamento);
      const fdNum = newRow.fator_diluicao
        ? parseFloat(normalizeDecimalInput(newRow.fator_diluicao))
        : undefined;

      // Fator obrigatório ainda vazio: preserva a leitura digitada sem chamar a API.
      if (precisaFd && fdNum === undefined) return newRow;

      setSalvando((prev) => ({ ...prev, [newRow.n_lab]: true }));

      try {
        const resposta = await entradaLoteService.salvarLeitura({
          analise: newRow.id,
          bateria: bateriaAtiva.id,
          leitura_bruta: leituraNum,
          ...(fdNum !== undefined && { fator_diluicao: fdNum }),
        });

        const linhaAtualizada: LinhaBancada = {
          ...newRow,
          resultado_preview: resposta.resultado_calculado ?? null,
          status: "salvo",
        };

        setLinhas((prev) =>
          prev.map((l) => (l.n_lab === newRow.n_lab ? linhaAtualizada : l)),
        );
        showSuccess(`Leitura de ${newRow.n_lab} salva.`);
        return linhaAtualizada;
      } catch (err) {
        const linhaComErro: LinhaBancada = { ...oldRow, status: "erro" };
        setLinhas((prev) =>
          prev.map((l) => (l.n_lab === oldRow.n_lab ? linhaComErro : l)),
        );
        showApiError(err);
        return linhaComErro;
      } finally {
        setSalvando((prev) => ({ ...prev, [newRow.n_lab]: false }));
      }
    },
    [bateriaAtiva, equipamento, elemento, showSuccess, showApiError, showError],
  );

  return {
    equipamento,
    setEquipamento,
    elemento,
    setElemento,
    bateriaAtiva,
    jaFiltrou,
    linhas,
    loadingAmostras,
    salvando,
    handleFiltrar,
    handleProcessRowUpdate,
  };
}

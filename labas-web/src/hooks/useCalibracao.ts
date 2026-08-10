import { useState, useEffect, useCallback } from "react";
import {
  calibracaoService,
  type BateriaCalibracaoComPontos,
  type CriarBateriaPayload,
} from "../services/calibracaoService";
import { useSnackbar } from "./useSnackbar";
import type { Equipamento } from "../types/calibracao";

/**
 * Gerencia a listagem de baterias de calibração com filtro por equipamento.
 * Após toggleAtivo, o backend altera o estado de múltiplas baterias,
 * então sempre fazemos refetch completo.
 */
export function useCalibracao(equipamentoInicial?: Equipamento) {
  const { showError, showSuccess, showApiError } = useSnackbar();
  const [baterias, setBaterias] = useState<BateriaCalibracaoComPontos[]>([]);
  const [loading, setLoading] = useState(true);
  const [equipamentoFiltro, setEquipamentoFiltro] = useState<
    Equipamento | undefined
  >(equipamentoInicial);

  const carregar = useCallback(async (signal?: AbortSignal) => {
    setLoading(true);
    try {
      const data = await calibracaoService.listarBaterias(equipamentoFiltro, signal);
      setBaterias(data);
    } catch (err) {
      if ((err as { code?: string })?.code === "ERR_CANCELED") return;
      showError("Erro ao carregar baterias de calibração.");
    } finally {
      setLoading(false);
    }
  }, [equipamentoFiltro, showError]);

  useEffect(() => {
    const controller = new AbortController();
    void carregar(controller.signal);
    return () => controller.abort();
  }, [carregar]);

  const criarBateria = useCallback(
    async (payload: CriarBateriaPayload) => {
      await calibracaoService.criarBateria(payload);
      showSuccess("Bateria criada com sucesso.");
      await carregar();
    },
    [carregar, showSuccess],
  );

  /**
   * Marca a bateria como ativo=true (ou false).
   * Sempre faz refetch pois o backend desativa as demais do mesmo elemento/equipamento.
   */
  const toggleAtivo = useCallback(
    async (id: number, ativo: boolean) => {
      try {
        await calibracaoService.toggleAtivo(id, ativo);
        showSuccess(ativo ? "Bateria ativada." : "Bateria desativada.");
        await carregar();
      } catch {
        showError("Erro ao atualizar bateria.");
      }
    },
    [carregar, showError, showSuccess],
  );

  const removerBateria = useCallback(
    async (id: number) => {
      try {
        await calibracaoService.removerBateria(id);
        showSuccess("Bateria removida.");
        await carregar();
      } catch (err) {
        showApiError(err);
      }
    },
    [carregar, showApiError, showError, showSuccess],
  );

  return {
    baterias,
    loading,
    equipamentoFiltro,
    setEquipamentoFiltro,
    criarBateria,
    toggleAtivo,
    removerBateria,
    recarregar: carregar,
  };
}

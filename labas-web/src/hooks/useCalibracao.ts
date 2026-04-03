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
export function useCalibracao() {
  const { showError, showSuccess } = useSnackbar();
  const [baterias, setBaterias] = useState<BateriaCalibracaoComPontos[]>([]);
  const [loading, setLoading] = useState(false);
  const [equipamentoFiltro, setEquipamentoFiltro] = useState<
    Equipamento | undefined
  >(undefined);

  const carregar = useCallback(async () => {
    setLoading(true);
    try {
      const data = await calibracaoService.listarBaterias(equipamentoFiltro);
      setBaterias(data);
    } catch {
      showError("Erro ao carregar baterias de calibração.");
    } finally {
      setLoading(false);
    }
  }, [equipamentoFiltro, showError]);

  useEffect(() => {
    carregar();
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
      } catch {
        showError("Erro ao remover bateria.");
      }
    },
    [carregar, showError, showSuccess],
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

import { useState, useEffect, useCallback } from "react";
import {
  calibracaoService,
  type BateriaCalibracaoComPontos,
  type AdicionarPontoPayload,
} from "../services/calibracaoService";
import { useSnackbar } from "./useSnackbar";

/**
 * Gerencia o detalhe de uma bateria individual com seus pontos.
 * adicionarPonto e removerPonto fazem refetch para refletir a equação
 * recalculada pelo backend via signal.
 */
export function useBateriaDetalhe(id: number | null) {
  const { showError, showSuccess } = useSnackbar();
  const [bateria, setBateria] = useState<BateriaCalibracaoComPontos | null>(
    null,
  );
  const [loading, setLoading] = useState(false);

  const carregar = useCallback(async () => {
    if (id === null) return;
    setLoading(true);
    try {
      const data = await calibracaoService.buscarBateria(id);
      setBateria(data);
    } catch {
      showError("Erro ao carregar bateria.");
    } finally {
      setLoading(false);
    }
  }, [id, showError]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  const adicionarPonto = useCallback(
    async (payload: AdicionarPontoPayload) => {
      if (!bateria) return;
      try {
        await calibracaoService.adicionarPonto(bateria.id, payload);
        showSuccess("Ponto adicionado. Equação recalculada.");
        await carregar();
      } catch {
        showError("Erro ao adicionar ponto.");
      }
    },
    [bateria, carregar, showError, showSuccess],
  );

  const removerPonto = useCallback(
    async (pontoId: number) => {
      try {
        await calibracaoService.removerPonto(pontoId);
        showSuccess("Ponto removido.");
        await carregar();
      } catch {
        showError("Erro ao remover ponto.");
      }
    },
    [carregar, showError, showSuccess],
  );

  return {
    bateria,
    loading,
    adicionarPonto,
    removerPonto,
    recarregar: carregar,
  };
}

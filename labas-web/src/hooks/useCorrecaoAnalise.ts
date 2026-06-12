import { useCallback, useEffect, useState } from "react";
import { correcaoService } from "../services/correcaoService";
import { analiseService } from "../services/analiseService";
import { useSnackbar } from "./useSnackbar";
import type {
  AnaliseSolo,
  LeituraDetalhe,
  LeituraCorrecaoPayload,
} from "../types/analise";

export interface UseCorrecaoAnaliseResult {
  analise: AnaliseSolo | null;
  leituras: LeituraDetalhe[];
  loading: boolean;
  salvando: boolean;
  corrigirLeitura: (
    leituraId: number,
    payload: LeituraCorrecaoPayload,
  ) => Promise<void>;
  salvarGranulometria: (payload: {
    areia?: number | null;
    argila?: number | null;
    silte?: number | null;
  }) => Promise<void>;
}

export function useCorrecaoAnalise(
  laudoId: number | undefined,
  analiseId: number | undefined,
): UseCorrecaoAnaliseResult {
  const { showSuccess, showApiError } = useSnackbar();
  const [analise, setAnalise] = useState<AnaliseSolo | null>(null);
  const [leituras, setLeituras] = useState<LeituraDetalhe[]>([]);
  const [loading, setLoading] = useState(false);
  const [salvando, setSalvando] = useState(false);

  const carregar = useCallback(async () => {
    if (!laudoId || !analiseId) return;
    setLoading(true);
    try {
      const [dadosAnalise, dadosLeituras] = await Promise.all([
        analiseService.buscar(laudoId, analiseId),
        correcaoService.listarLeituras(analiseId),
      ]);
      setAnalise(dadosAnalise);
      setLeituras(dadosLeituras);
    } catch (err) {
      showApiError(err);
    } finally {
      setLoading(false);
    }
  }, [laudoId, analiseId, showApiError]);

  useEffect(() => {
    void carregar();
  }, [carregar]);

  const corrigirLeitura = useCallback(
    async (leituraId: number, payload: LeituraCorrecaoPayload) => {
      setSalvando(true);
      try {
        const atualizada = await correcaoService.corrigirLeitura(
          leituraId,
          payload,
        );
        setLeituras((prev) =>
          prev.map((l) => (l.id === leituraId ? atualizada : l)),
        );
        // Re-carrega a analise para refletir os índices recalculados (SB, CTC, V%...)
        if (laudoId && analiseId) {
          const analiseAtualizada = await analiseService.buscar(
            laudoId,
            analiseId,
          );
          setAnalise(analiseAtualizada);
        }
        showSuccess("Leitura corrigida. Índices recalculados.");
      } catch (err) {
        showApiError(err);
      } finally {
        setSalvando(false);
      }
    },
    [laudoId, analiseId, showSuccess, showApiError],
  );

  const salvarGranulometria = useCallback(
    async (payload: {
      areia?: number | null;
      argila?: number | null;
      silte?: number | null;
    }) => {
      if (!laudoId || !analiseId) return;
      setSalvando(true);
      try {
        const atualizada = await analiseService.atualizar(
          laudoId,
          analiseId,
          payload,
        );
        setAnalise(atualizada);
        showSuccess("Granulometria salva.");
      } catch (err) {
        showApiError(err);
      } finally {
        setSalvando(false);
      }
    },
    [laudoId, analiseId, showSuccess, showApiError],
  );

  return {
    analise,
    leituras,
    loading,
    salvando,
    corrigirLeitura,
    salvarGranulometria,
  };
}

import { useCallback, useEffect, useState } from "react";
import { analiseService } from "../services/analiseService";
import { useSnackbar } from "./useSnackbar";
import type { AnaliseSolo, AnaliseSoloPayload } from "../types/analise";

export interface UseAnalisesResult {
  analises: AnaliseSolo[];
  loading: boolean;
  salvando: boolean;
  editando: number | null;
  removendo: number | null;
  criar: (payload: Omit<AnaliseSoloPayload, "laudo_id">) => Promise<void>;
  editar: (
    analiseId: number,
    payload: Partial<Omit<AnaliseSoloPayload, "laudo_id">>,
  ) => Promise<void>;
  toggleAtivo: (analiseId: number, ativo: boolean) => Promise<void>;
  remover: (analiseId: number) => Promise<void>;
  recarregar: () => void;
}

export function useAnalises(laudoId: number | undefined): UseAnalisesResult {
  const { showSuccess, showApiError } = useSnackbar();
  const [analises, setAnalises] = useState<AnaliseSolo[]>([]);
  const [loading, setLoading] = useState(true);
  const [salvando, setSalvando] = useState(false);
  const [editando, setEditando] = useState<number | null>(null);
  const [removendo, setRemovendo] = useState<number | null>(null);

  const carregar = useCallback(async () => {
    if (!laudoId) return;
    setLoading(true);
    try {
      const data = await analiseService.listar(laudoId);
      setAnalises(data);
    } catch (err) {
      showApiError(err);
    } finally {
      setLoading(false);
    }
  }, [laudoId, showApiError]);

  useEffect(() => {
    void carregar();
  }, [carregar]);

  const criar = useCallback(
    async (payload: Omit<AnaliseSoloPayload, "laudo_id">) => {
      if (!laudoId) return;
      setSalvando(true);
      try {
        const novaAnalise = await analiseService.criar(laudoId, payload);
        setAnalises((prev) => [...prev, novaAnalise]);
        showSuccess("Análise adicionada com sucesso.");
      } catch (err) {
        showApiError(err);
      } finally {
        setSalvando(false);
      }
    },
    [laudoId, showSuccess, showApiError],
  );

  const editar = useCallback(
    async (
      analiseId: number,
      payload: Partial<Omit<AnaliseSoloPayload, "laudo_id">>,
    ) => {
      if (!laudoId) return;
      setEditando(analiseId);
      try {
        const atualizada = await analiseService.atualizar(
          laudoId,
          analiseId,
          payload,
        );
        setAnalises((prev) =>
          prev.map((a) => (a.id === analiseId ? atualizada : a)),
        );
        showSuccess("Análise atualizada com sucesso.");
      } catch (err) {
        showApiError(err);
      } finally {
        setEditando(null);
      }
    },
    [laudoId, showSuccess, showApiError],
  );

  const toggleAtivo = useCallback(
    async (analiseId: number, ativo: boolean) => {
      if (!laudoId) return;
      try {
        const atualizada = await analiseService.toggleAtivo(
          laudoId,
          analiseId,
          ativo,
        );
        setAnalises((prev) =>
          prev.map((a) => (a.id === analiseId ? atualizada : a)),
        );
      } catch (err) {
        showApiError(err);
      }
    },
    [laudoId, showApiError],
  );

  const remover = useCallback(
    async (analiseId: number) => {
      if (!laudoId) return;
      setRemovendo(analiseId);
      try {
        await analiseService.remover(laudoId, analiseId);
        setAnalises((prev) => prev.filter((a) => a.id !== analiseId));
        showSuccess("Análise removida.");
      } catch (err) {
        showApiError(err);
      } finally {
        setRemovendo(null);
      }
    },
    [laudoId, showSuccess, showApiError],
  );

  return {
    analises,
    loading,
    salvando,
    editando,
    removendo,
    criar,
    editar,
    toggleAtivo,
    remover,
    recarregar: carregar,
  };
}

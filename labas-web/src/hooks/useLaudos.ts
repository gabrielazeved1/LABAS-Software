import { useEffect, useState, useCallback } from "react";
import { laudoService } from "../services/laudoService";
import type { AnaliseSolo, AnaliseSoloPayload } from "../types/analise";
import { parseError } from "../utils/parseError";

// Estado tipado e preparado para evolução (ex: paginação futura)
type State = {
  data: AnaliseSolo[];
  loading: boolean;
  error: string | null;
};

export function useLaudos() {
  const [state, setState] = useState<State>({
    data: [],
    loading: false,
    error: null,
  });

  //LISTAR LAUDOS
  const fetchLaudos = useCallback(async () => {
    // evita chamadas concorrentes desnecessárias
    if (state.loading) return;

    setState((s) => ({
      ...s,
      loading: true,
      error: null,
    }));

    try {
      const data = await laudoService.listarLaudos();

      // NÃO sobrescreve o estado inteiro (importante para escalabilidade)
      setState((s) => ({
        ...s,
        data,
        loading: false,
        error: null,
      }));
    } catch (err: unknown) {
      const message = parseError(err);

      setState((s) => ({
        ...s,
        loading: false,
        error: message,
      }));
    }
  }, [state.loading]);

  //CRIAR LAUDO
  const createLaudo = useCallback(async (payload: AnaliseSoloPayload) => {
    try {
      const created = await laudoService.criarLaudo(payload);

      // adiciona diretamente no estado
      setState((s) => ({
        ...s,
        data: [created, ...s.data],
      }));

      return created;
    } catch (err: unknown) {
      throw parseError(err);
    }
  }, []);

  // EDITAR LAUDO
  const updateLaudo = useCallback(
    async (n_lab: string, payload: Partial<AnaliseSoloPayload>) => {
      try {
        const updated = await laudoService.editarLaudo(n_lab, payload);

        // substitui apenas o item alterado
        setState((s) => ({
          ...s,
          data: s.data.map((l) =>
            l.n_lab === n_lab ? updated : l
          ),
        }));

        return updated;
      } catch (err: unknown) {
        throw parseError(err);
      }
    },
    []
  );

  // DELETAR LAUDO
  const deleteLaudo = useCallback(async (n_lab: string) => {
    try {
      await laudoService.deletarLaudo(n_lab);
      
      setState((s) => ({
        ...s,
        data: s.data.filter((l) => l.n_lab !== n_lab),
      }));
    } catch (err: unknown) {
      throw parseError(err);
    }
  }, []);

  // GERAR PDF
  const downloadPdf = useCallback(async (n_lab: string) => {
    try {
      const blob = await laudoService.gerarPDF(n_lab);

      // responsabilidade do hook: abrir/download automático
      const url = window.URL.createObjectURL(blob);
      window.open(url);

      // libera memória
      window.URL.revokeObjectURL(url);
    } catch (err: unknown) {
      throw parseError(err);
    }
  }, []);

  // carregamento inicial
  useEffect(() => {
    fetchLaudos();
  }, [fetchLaudos]);

  return {
    ...state,
    refetch: fetchLaudos,
    createLaudo,
    updateLaudo,
    deleteLaudo,
    downloadPdf,
  };
}
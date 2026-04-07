import { useCallback, useEffect, useState } from "react";
import { laudoService } from "../services/laudoService";
import { useSnackbar } from "./useSnackbar";
import type { AnaliseSolo } from "../types/analise";

export interface UseLaudosResult {
  laudos: AnaliseSolo[];
  loading: boolean;
  deletando: string | null; // n_lab sendo deletado (para loading por linha)
  baixarPdf: (nLab: string) => Promise<void>;
  excluir: (nLab: string) => Promise<void>;
  recarregar: () => void;
}

const criarNomeArquivo = (nLab: string) =>
  `laudo_${nLab.replace("/", "-")}.pdf`;

export function useLaudos(): UseLaudosResult {
  const { showSuccess, showApiError } = useSnackbar();
  const [laudos, setLaudos] = useState<AnaliseSolo[]>([]);
  const [loading, setLoading] = useState(true);
  const [deletando, setDeletando] = useState<string | null>(null);

  const carregar = useCallback(async () => {
    setLoading(true);
    try {
      const response = await laudoService.listar();
      setLaudos(response.results);
    } catch (err) {
      showApiError(err);
    } finally {
      setLoading(false);
    }
  }, [showApiError]);

  useEffect(() => {
    void carregar();
  }, [carregar]);

  const baixarPdf = useCallback(
    async (nLab: string) => {
      try {
        const blob = await laudoService.baixarPdf(nLab);
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = criarNomeArquivo(nLab);
        link.style.display = "none";
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
      } catch (err) {
        showApiError(err);
      }
    },
    [showApiError],
  );

  const excluir = useCallback(
    async (nLab: string) => {
      setDeletando(nLab);
      try {
        await laudoService.remover(nLab);
        showSuccess(`Laudo ${nLab} excluído com sucesso.`);
        setLaudos((prev) => prev.filter((l) => l.n_lab !== nLab));
      } catch (err) {
        showApiError(err);
      } finally {
        setDeletando(null);
      }
    },
    [showSuccess, showApiError],
  );

  return {
    laudos,
    loading,
    deletando,
    baixarPdf,
    excluir,
    recarregar: carregar,
  };
}

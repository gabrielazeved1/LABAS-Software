import { useCallback, useEffect, useState } from "react";
import { laudoService } from "../services/laudoService";
import { useSnackbar } from "./useSnackbar";
import type { Laudo } from "../types/analise";

export interface UseLaudosResult {
  laudos: Laudo[];
  loading: boolean;
  deletando: number | null;
  baixarPdf: (id: number, codigoLaudo: string) => Promise<void>;
  excluir: (id: number) => Promise<void>;
  recarregar: () => void;
}

const criarNomeArquivo = (codigoLaudo: string) =>
  `laudo_${codigoLaudo.replace("/", "-")}.pdf`;

export function useLaudos(): UseLaudosResult {
  const { showSuccess, showApiError } = useSnackbar();
  const [laudos, setLaudos] = useState<Laudo[]>([]);
  const [loading, setLoading] = useState(true);
  const [deletando, setDeletando] = useState<number | null>(null);

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
    async (id: number, codigoLaudo: string) => {
      try {
        const blob = await laudoService.baixarPdf(id);
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = criarNomeArquivo(codigoLaudo);
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
    async (id: number) => {
      setDeletando(id);
      try {
        await laudoService.remover(id);
        showSuccess("Laudo excluído com sucesso.");
        setLaudos((prev) => prev.filter((l) => l.id !== id));
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

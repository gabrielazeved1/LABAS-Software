import { useCallback, useEffect, useState } from "react";
import { laudoService } from "../services/laudoService";
import type { AnaliseSolo } from "../types/analise";

interface UseLaudosResult {
  laudos: AnaliseSolo[];
  loading: boolean;
  baixarPdf: (nLab: string) => Promise<void>;
}

const criarNomeArquivo = (nLab: string) =>
  `laudo_${nLab.replace("/", "-")}.pdf`;

export function useLaudos(): UseLaudosResult {
  const [laudos, setLaudos] = useState<AnaliseSolo[]>([]);
  const [loading, setLoading] = useState(true);

  const carregar = useCallback(async () => {
    setLoading(true);
    const response = await laudoService.listarMeusLaudos();
    setLaudos(response.results);
    setLoading(false);
  }, []);

  useEffect(() => {
    void carregar();
  }, [carregar]);

  const baixarPdf = useCallback(async (nLab: string) => {
    const blob = await laudoService.baixarPdfLaudo(nLab);
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = criarNomeArquivo(nLab);
    link.style.display = "none";
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  }, []);

  return { laudos, loading, baixarPdf };
}

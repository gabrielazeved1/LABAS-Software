import { useCallback, useEffect, useState } from "react";
import { dashboardService } from "../services/dashboardService";
import { useSnackbar } from "./useSnackbar";
import type { LaudoResumo } from "../types/dashboard";

export interface UseDashboardLaudosResult {
  laudos: LaudoResumo[];
  loading: boolean;
  erro: string | null;
  recarregar: () => void;
}

export function useDashboardLaudos(): UseDashboardLaudosResult {
  const { showApiError } = useSnackbar();
  const [laudos, setLaudos] = useState<LaudoResumo[]>([]);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState<string | null>(null);

  const carregar = useCallback(async () => {
    setLoading(true);
    setErro(null);
    try {
      const data = await dashboardService.buscarLaudosRecentes();
      setLaudos(data);
    } catch (err) {
      setErro("Não foi possível carregar os laudos recentes.");
      showApiError(err);
    } finally {
      setLoading(false);
    }
  }, [showApiError]);

  useEffect(() => {
    void carregar();
  }, [carregar]);

  return { laudos, loading, erro, recarregar: carregar };
}

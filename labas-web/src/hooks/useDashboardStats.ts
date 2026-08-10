import { useCallback, useEffect, useState } from "react";
import { dashboardService } from "../services/dashboardService";
import { useSnackbar } from "./useSnackbar";
import type { DashboardStats } from "../types/dashboard";

export interface UseDashboardStatsResult {
  stats: DashboardStats | null;
  loading: boolean;
  erro: string | null;
  recarregar: () => void;
}

export function useDashboardStats(): UseDashboardStatsResult {
  const { showApiError } = useSnackbar();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState<string | null>(null);

  const carregar = useCallback(async (signal?: AbortSignal) => {
    setLoading(true);
    setErro(null);
    try {
      const data = await dashboardService.buscarStats(signal);
      setStats(data);
    } catch (err) {
      if ((err as { code?: string })?.code === "ERR_CANCELED") return;
      setErro("Não foi possível carregar os indicadores.");
      showApiError(err);
    } finally {
      setLoading(false);
    }
  }, [showApiError]);

  useEffect(() => {
    const controller = new AbortController();
    void carregar(controller.signal);
    return () => controller.abort();
  }, [carregar]);

  return { stats, loading, erro, recarregar: carregar };
}

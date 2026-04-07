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

  const carregar = useCallback(async () => {
    setLoading(true);
    setErro(null);
    try {
      const data = await dashboardService.buscarStats();
      setStats(data);
    } catch (err) {
      setErro("Não foi possível carregar os indicadores.");
      showApiError(err);
    } finally {
      setLoading(false);
    }
  }, [showApiError]);

  useEffect(() => {
    void carregar();
  }, [carregar]);

  return { stats, loading, erro, recarregar: carregar };
}

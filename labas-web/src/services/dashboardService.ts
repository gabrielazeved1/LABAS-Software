import { api } from "./api";
import type { DashboardStats, LaudoResumo } from "../types/dashboard";

export const dashboardService = {
  async buscarStats(signal?: AbortSignal): Promise<DashboardStats> {
    const { data } = await api.get<DashboardStats>("/dashboard/stats/", { signal });
    return data;
  },

  async buscarLaudosRecentes(signal?: AbortSignal): Promise<LaudoResumo[]> {
    const { data } = await api.get<LaudoResumo[]>(
      "/dashboard/laudos-recentes/",
      { signal },
    );
    return data;
  },
};

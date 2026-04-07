import { api } from "./api";
import type { DashboardStats, LaudoResumo } from "../types/dashboard";

export const dashboardService = {
  async buscarStats(): Promise<DashboardStats> {
    const { data } = await api.get<DashboardStats>("/dashboard/stats/");
    return data;
  },

  async buscarLaudosRecentes(): Promise<LaudoResumo[]> {
    const { data } = await api.get<LaudoResumo[]>(
      "/dashboard/laudos-recentes/",
    );
    return data;
  },
};

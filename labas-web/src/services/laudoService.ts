import { api } from "./api";
import type { Laudo, LaudoPayload, PaginatedResponse } from "../types/analise";

const BASE = "/laudos/";

export const laudoService = {
  async listar(page?: number): Promise<PaginatedResponse<Laudo>> {
    const { data } = await api.get(BASE, {
      params: page ? { page } : undefined,
    });
    if (Array.isArray(data)) {
      return { count: data.length, next: null, previous: null, results: data };
    }
    return data as PaginatedResponse<Laudo>;
  },

  async buscar(id: number): Promise<Laudo> {
    const { data } = await api.get<Laudo>(`${BASE}${id}/`);
    return data;
  },

  async criar(payload: LaudoPayload): Promise<Laudo> {
    const { data } = await api.post<Laudo>(BASE, payload);
    return data;
  },

  async atualizar(id: number, payload: Partial<LaudoPayload>): Promise<Laudo> {
    const { data } = await api.patch<Laudo>(`${BASE}${id}/`, payload);
    return data;
  },

  async remover(id: number): Promise<void> {
    await api.delete(`${BASE}${id}/`);
  },

  async baixarPdf(id: number): Promise<Blob> {
    const { data } = await api.get(`${BASE}${id}/pdf/`, {
      responseType: "blob",
    });
    return data as Blob;
  },
};

import { api } from "./api";
import type { Laudo, LaudoPayload, PaginatedResponse } from "../types/analise";

const BASE = "/laudos/";

export const laudoService = {
  async listar(page?: number, signal?: AbortSignal): Promise<PaginatedResponse<Laudo>> {
    const { data } = await api.get(BASE, {
      params: page ? { page } : undefined,
      signal,
    });
    if (Array.isArray(data)) {
      return { count: data.length, next: null, previous: null, results: data };
    }
    return data as PaginatedResponse<Laudo>;
  },

  async buscarPorCodigo(search: string, signal?: AbortSignal): Promise<Laudo[]> {
    const { data } = await api.get(BASE, { params: { search }, signal });
    const result = Array.isArray(data) ? data : (data.results ?? []);
    return result as Laudo[];
  },

  async buscar(id: number, signal?: AbortSignal): Promise<Laudo> {
    const { data } = await api.get<Laudo>(`${BASE}${id}/`, { signal });
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

  enviarPorEmail: async (id: number): Promise<void> => {
    await api.post(`/laudos/${id}/enviar-email/`);
  },

  async baixarPdf(id: number): Promise<Blob> {
    const { data } = await api.get(`${BASE}${id}/pdf/?modo=analise`, {
      responseType: "blob",
    });
    return data as Blob;
  },

  async baixarPdfCompleto(id: number, conjuntoId?: number): Promise<Blob> {
    const params = new URLSearchParams({ modo: "padrao_mais_analise" });
    if (conjuntoId) params.append("conjunto", String(conjuntoId));
    const { data } = await api.get(`${BASE}${id}/pdf/?${params.toString()}`, {
      responseType: "blob",
    });
    return data as Blob;
  },
};

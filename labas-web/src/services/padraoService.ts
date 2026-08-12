import { api } from "./api";
import type { ConjuntoPadrao, PadraoPayload } from "../types/padroes";

const BASE = "/conjuntos-padrao/";

export const padraoService = {
  async listar(): Promise<ConjuntoPadrao[]> {
    const { data } = await api.get<ConjuntoPadrao[]>(BASE);
    return data;
  },

  async buscar(id: number): Promise<ConjuntoPadrao> {
    const { data } = await api.get<ConjuntoPadrao>(`${BASE}${id}/`);
    return data;
  },

  async criar(nome: string): Promise<ConjuntoPadrao> {
    const { data } = await api.post<ConjuntoPadrao>(BASE, { nome });
    return data;
  },

  async renomear(id: number, nome: string): Promise<ConjuntoPadrao> {
    const { data } = await api.patch<ConjuntoPadrao>(`${BASE}${id}/`, { nome });
    return data;
  },

  async remover(id: number): Promise<void> {
    await api.delete(`${BASE}${id}/`);
  },

  async ativar(id: number): Promise<ConjuntoPadrao> {
    const { data } = await api.post<ConjuntoPadrao>(`${BASE}${id}/ativar/`);
    return data;
  },

  async desativar(id: number): Promise<ConjuntoPadrao> {
    const { data } = await api.post<ConjuntoPadrao>(`${BASE}${id}/desativar/`);
    return data;
  },

  async atualizarPadrao(
    conjuntoId: number,
    tipo: string,
    payload: PadraoPayload,
  ): Promise<void> {
    await api.put(`${BASE}${conjuntoId}/padroes/${tipo}/`, payload);
  },

  async baixarPdf(id: number): Promise<Blob> {
    const { data } = await api.get(`${BASE}${id}/pdf/`, { responseType: "blob" });
    return data as Blob;
  },
};

import { api } from "./api";
import type { AnaliseSolo, AnaliseSoloPayload } from "../types/analise";

const BASE = "/meus-laudos/";

export const laudoService = {
  async listarLaudos(): Promise<AnaliseSolo[]> {
    const { data } = await api.get(BASE);
    return Array.isArray(data) ? data : (data.results ?? []);
  },

  async criarLaudo(payload: AnaliseSoloPayload): Promise<AnaliseSolo> {
    const { data } = await api.post<AnaliseSolo>(BASE, payload);
    return data;
  },

  async buscarLaudo(n_lab: string): Promise<AnaliseSolo> {
    const { data } = await api.get<AnaliseSolo>(`${BASE}${n_lab}/`);
    return data;
  },

  async editarLaudo(n_lab: string, payload: Partial<AnaliseSoloPayload>): Promise<AnaliseSolo> {
    const { data } = await api.put<AnaliseSolo>(`${BASE}${n_lab}/`, payload);
    return data;
  },

  async deletarLaudo(n_lab: string): Promise<void> {
    await api.delete(`${BASE}${n_lab}/`);
  },

  async gerarPDF(n_lab: string): Promise<Blob> {
    const { data } = await api.get(`${BASE}${n_lab}/pdf/`, { responseType: "blob" });
    return data;
  },
};
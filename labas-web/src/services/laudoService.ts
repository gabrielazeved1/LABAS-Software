import { api } from "./api";
import type {
  AnaliseSolo,
  AnaliseSoloPayload,
  PaginatedResponse,
} from "../types/analise";

const BASE = "/meus-laudos/";

const normalizarNLab = (nLab: string) => nLab.replace(/^\/+|\/+$/g, "");

export const laudoService = {
  /** Lista laudos com paginação padrão do DRF. */
  async listar(page?: number): Promise<PaginatedResponse<AnaliseSolo>> {
    const { data } = await api.get(BASE, {
      params: page ? { page } : undefined,
    });
    if (Array.isArray(data)) {
      return { count: data.length, next: null, previous: null, results: data };
    }
    return data as PaginatedResponse<AnaliseSolo>;
  },

  /** Lista os laudos do cliente logado (rota /meus-laudos/). */
  async listarMeusLaudos(): Promise<PaginatedResponse<AnaliseSolo>> {
    const { data } = await api.get(BASE);
    if (Array.isArray(data)) {
      return { count: data.length, next: null, previous: null, results: data };
    }
    return data as PaginatedResponse<AnaliseSolo>;
  },

  /** Cria um novo laudo (somente staff). */
  async criar(payload: AnaliseSoloPayload): Promise<AnaliseSolo> {
    const { data } = await api.post<AnaliseSolo>(BASE, payload);
    return data;
  },

  /** Busca detalhe de um laudo pelo N Lab. */
  async buscar(nLab: string): Promise<AnaliseSolo> {
    const { data } = await api.get<AnaliseSolo>(
      `${BASE}${normalizarNLab(nLab)}/`,
    );
    return data;
  },

  /** Atualiza parcialmente um laudo (somente staff). */
  async atualizar(
    nLab: string,
    payload: Partial<AnaliseSoloPayload>,
  ): Promise<AnaliseSolo> {
    const { data } = await api.patch<AnaliseSolo>(
      `${BASE}${normalizarNLab(nLab)}/`,
      payload,
    );
    return data;
  },

  /** Remove um laudo (somente staff). */
  async remover(nLab: string): Promise<void> {
    await api.delete(`${BASE}${normalizarNLab(nLab)}/`);
  },

  /** Gera o PDF oficial do laudo. */
  async baixarPdf(nLab: string): Promise<Blob> {
    const { data } = await api.get(`${BASE}${normalizarNLab(nLab)}/pdf/`, {
      responseType: "blob",
    });
    return data as Blob;
  },

  /** Baixa o PDF do laudo do cliente logado. */
  async baixarPdfLaudo(nLab: string): Promise<Blob> {
    const { data } = await api.get(`${BASE}${normalizarNLab(nLab)}/pdf/`, {
      responseType: "blob",
    });
    return data as Blob;
  },
};

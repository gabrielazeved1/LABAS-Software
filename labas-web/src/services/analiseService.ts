import { api } from "./api";
import type { AnaliseSolo, AnaliseSoloPayload } from "../types/analise";

const base = (laudoId: number) => `/laudos/${laudoId}/analises/`;

export const analiseService = {
  async listar(laudoId: number): Promise<AnaliseSolo[]> {
    const { data } = await api.get<AnaliseSolo[]>(base(laudoId));
    return data;
  },

  async buscar(laudoId: number, analiseId: number): Promise<AnaliseSolo> {
    const { data } = await api.get<AnaliseSolo>(
      `${base(laudoId)}${analiseId}/`,
    );
    return data;
  },

  async criar(
    laudoId: number,
    payload: Partial<AnaliseSoloPayload>,
  ): Promise<AnaliseSolo> {
    const { data } = await api.post<AnaliseSolo>(base(laudoId), payload);
    return data;
  },

  async atualizar(
    laudoId: number,
    analiseId: number,
    payload: Partial<AnaliseSoloPayload>,
  ): Promise<AnaliseSolo> {
    const { data } = await api.patch<AnaliseSolo>(
      `${base(laudoId)}${analiseId}/`,
      payload,
    );
    return data;
  },

  async remover(laudoId: number, analiseId: number): Promise<void> {
    await api.delete(`${base(laudoId)}${analiseId}/`);
  },

  /** Alterna o flag ativo de uma análise (staff only). */
  async toggleAtivo(
    laudoId: number,
    analiseId: number,
    ativo: boolean,
  ): Promise<AnaliseSolo> {
    const { data } = await api.patch<AnaliseSolo>(
      `${base(laudoId)}${analiseId}/`,
      { ativo },
    );
    return data;
  },
};

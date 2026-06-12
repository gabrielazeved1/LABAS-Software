import { api } from "./api";
import type { LeituraDetalhe, LeituraCorrecaoPayload } from "../types/analise";

export const correcaoService = {
  /** Lista todas as leituras brutas registradas para uma AnaliseSolo. */
  async listarLeituras(analiseId: number): Promise<LeituraDetalhe[]> {
    const { data } = await api.get<LeituraDetalhe[]>(
      `/analises/${analiseId}/leituras/`,
    );
    return data;
  },

  /** Corrige leitura_bruta e/ou fator_diluicao; backend re-dispara o signal. */
  async corrigirLeitura(
    leituraId: number,
    payload: LeituraCorrecaoPayload,
  ): Promise<LeituraDetalhe> {
    const { data } = await api.patch<LeituraDetalhe>(
      `/leituras/${leituraId}/`,
      payload,
    );
    return data;
  },
};

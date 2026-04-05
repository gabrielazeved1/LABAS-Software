import { api } from "./api";
import type { Equipamento, Elemento } from "../types/calibracao";
import type {
  AmostraPendente,
  LeituraPayload,
  LeituraResponse,
} from "../types/entradaLote";

const BASE_AMOSTRAS = "/amostras/";
const BASE_LEITURAS = "/leituras/";

export const entradaLoteService = {
  /**
   * Busca as AnaliseSolo que ainda não possuem leitura registrada
   * para a bateria ativa do equipamento/elemento informado.
   */
  async buscarAmostrasPendentes(
    equipamento: Equipamento,
    elemento: Elemento,
  ): Promise<AmostraPendente[]> {
    const { data } = await api.get(BASE_AMOSTRAS, {
      params: { equipamento, elemento },
    });
    return Array.isArray(data) ? data : (data.results ?? []);
  },

  /**
   * Registra a leitura bruta de uma amostra na bancada.
   * O signal do backend dispara o cálculo e persiste o resultado na AnaliseSolo.
   */
  async salvarLeitura(payload: LeituraPayload): Promise<LeituraResponse> {
    const { data } = await api.post<LeituraResponse>(BASE_LEITURAS, payload);
    return data;
  },
};

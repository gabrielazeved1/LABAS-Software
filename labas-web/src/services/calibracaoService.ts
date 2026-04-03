import { api } from "./api";
import type {
  BateriaCalibracao,
  PontoCalibracao,
  Equipamento,
} from "../types/calibracao";

export interface BateriaCalibracaoComPontos extends BateriaCalibracao {
  pontos: PontoCalibracao[];
}

export interface CriarBateriaPayload {
  equipamento: Equipamento;
  elemento: string;
  volume_solo?: number | null;
  volume_extrator?: number | null;
  leitura_branco?: number | null;
  ativo?: boolean;
}

export interface AdicionarPontoPayload {
  concentracao: number;
  absorvancia: number;
  bateria: number;
}

const BASE = "/baterias/";

export const calibracaoService = {
  /** Lista baterias. Filtra por equipamento quando fornecido. Garante array mesmo com paginação DRF. */
  async listarBaterias(
    equipamento?: Equipamento,
  ): Promise<BateriaCalibracaoComPontos[]> {
    const params = equipamento ? { equipamento } : {};
    const { data } = await api.get(BASE, { params });
    // Se vier paginado, retorna data.results, senão data
    return Array.isArray(data) ? data : (data.results ?? []);
  },

  /** Cria nova bateria de calibração. */
  async criarBateria(
    payload: CriarBateriaPayload,
  ): Promise<BateriaCalibracaoComPontos> {
    const { data } = await api.post<BateriaCalibracaoComPontos>(BASE, payload);
    return data;
  },

  /** Busca detalhe de uma bateria com seus pontos aninhados. */
  async buscarBateria(id: number): Promise<BateriaCalibracaoComPontos> {
    const { data } = await api.get<BateriaCalibracaoComPontos>(`${BASE}${id}/`);
    return data;
  },

  /**
   * Ativa uma bateria via PATCH { ativo: true }.
   * O backend desativa automaticamente as demais do mesmo elemento/equipamento.
   */
  async toggleAtivo(id: number, ativo: boolean): Promise<BateriaCalibracao> {
    const { data } = await api.patch<BateriaCalibracao>(`${BASE}${id}/`, {
      ativo,
    });
    return data;
  },

  /** Remove uma bateria e todos os seus pontos. */
  async removerBateria(id: number): Promise<void> {
    await api.delete(`${BASE}${id}/`);
  },

  /** Adiciona um ponto de calibração a uma bateria. Dispara recálculo da equação. */
  async adicionarPonto(
    bateriaId: number,
    payload: AdicionarPontoPayload,
  ): Promise<PontoCalibracao> {
    const { data } = await api.post<PontoCalibracao>(
      `${BASE}${bateriaId}/pontos/`,
      payload,
    );
    return data;
  },

  /** Remove um ponto específico. Dispara recálculo da equação. */
  async removerPonto(pontoId: number): Promise<void> {
    await api.delete(`/pontos/${pontoId}/`);
  },
};

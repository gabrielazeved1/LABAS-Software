import { api } from "./api";
import type {
  BateriaCalibracao,
  PontoCalibracao,
  Equipamento,
  Elemento,
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
}

export interface AtualizarBateriaPayload {
  volume_solo?: number | null;
  volume_extrator?: number | null;
  leitura_branco?: number | null;
}

export interface AdicionarPontoPayload {
  concentracao: number;
  absorvancia: number;
  bateria: number;
}

const BASE = "/baterias/";

export const calibracaoService = {
  /** Lista baterias. Filtra por equipamento e/ou elemento quando fornecido. */
  async listarBaterias(
    equipamento?: Equipamento,
    elemento?: Elemento,
    signal?: AbortSignal,
  ): Promise<BateriaCalibracaoComPontos[]> {
    const params: Record<string, string> = {};
    if (equipamento) params.equipamento = equipamento;
    if (elemento) params.elemento = elemento;
    const { data } = await api.get(BASE, { params, signal });
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
  async buscarBateria(id: number, signal?: AbortSignal): Promise<BateriaCalibracaoComPontos> {
    const { data } = await api.get<BateriaCalibracaoComPontos>(`${BASE}${id}/`, { signal });
    return data;
  },

  /** Remove uma bateria e todos os seus pontos. */
  async removerBateria(id: number): Promise<void> {
    await api.delete(`${BASE}${id}/`);
  },

  /** Atualiza parâmetros da bateria (volumes, branco). */
  async atualizarBateria(
    id: number,
    payload: AtualizarBateriaPayload,
  ): Promise<BateriaCalibracaoComPontos> {
    const { data } = await api.patch<BateriaCalibracaoComPontos>(
      `${BASE}${id}/`,
      payload,
    );
    return data;
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

import type { Equipamento, Elemento } from "./calibracao";

/**
 * Representação mínima de uma AnaliseSolo pendente de leitura na bancada.
 * Espelha o AmostraPendenteSerializer do backend.
 */
export interface AmostraPendente {
  id: number;
  n_lab: string;
  cliente_nome: string;
  data_entrada: string;
}

/**
 * Payload para registrar uma leitura bruta no backend.
 * Espelha o LeituraEquipamentoSerializer do backend.
 */
export interface LeituraPayload {
  analise: number;
  bateria: number;
  leitura_bruta: number;
  fator_diluicao?: number;
}

/**
 * Resposta do backend após criação de uma LeituraEquipamento.
 * `resultado_calculado` é retornado pelo serializer com o valor já processado
 * pelo signal do backend (campo calculado da AnaliseSolo).
 */
export interface LeituraResponse {
  id: number;
  analise: number;
  bateria: number;
  leitura_bruta: number;
  fator_diluicao: number | null;
  resultado_calculado?: number | null;
}

/**
 * Tipo exclusivo da UI — estado de cada linha do DataGrid da bancada.
 * Agrega os dados da amostra com os campos de entrada do técnico
 * e o resultado calculado em tempo real no cliente.
 */
export interface LinhaBancada extends AmostraPendente {
  /** Equipamento ativo no filtro atual */
  equipamento: Equipamento;
  /** Elemento ativo no filtro atual */
  elemento: Elemento;
  /** Leitura bruta digitada pelo técnico (Absorvância, Emissão, Transmitância...) */
  leitura_bruta: string;
  /** Fator de diluição digitado (obrigatório para AA, FC, ES) */
  fator_diluicao: string;
  /** Resultado calculado em tempo real pelo cliente antes do envio */
  resultado_preview: number | null;
  /** Estado de persistência da linha */
  status: "pendente" | "salvo" | "erro";
}

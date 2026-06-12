import type { Cliente } from "./cliente";

// ─── Resposta paginada DRF ────────────────────────────────────────────────────

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// ─── Laudo (cabeçalho) ────────────────────────────────────────────────────────

/** Cabeçalho do documento entregue ao cliente. Pai de N análises. */
export interface Laudo {
  id: number;
  /** Código gerado pelo backend: "L-AAAA/N" — read-only */
  codigo_laudo: string;
  cliente: Cliente;
  /** Usado apenas no payload de criação/edição */
  cliente_codigo?: string;
  /** Data de entrada das amostras no laboratório */
  data_emissao: string;
  /** Data de saída (laudo disponível ao cliente) — nullable */
  data_saida: string | null;
  observacoes: string | null;
}

export type LaudoPayload = {
  cliente_codigo: string;
  data_emissao: string;
  data_saida?: string | null;
  observacoes?: string | null;
};

// ─── AnaliseSolo (amostra individual, filho de Laudo) ─────────────────────────

export interface AnaliseSolo {
  id: number;
  laudo_id: number;
  n_lab: string;
  ativo: boolean;
  referencia: string | null;
  data_entrada: string;
  data_saida: string | null;

  // pH-metro
  ph_agua: number | null;
  ph_cacl2: number | null;
  ph_kcl: number | null;

  // Espectrofotômetro
  p_m: number | null;
  p_r: number | null;
  p_rem: number | null;
  mo: number | null;
  s: number | null;
  b: number | null;

  // Fotômetro de Chama
  k: number | null;
  na: number | null;

  // Absorção Atômica
  ca: number | null;
  mg: number | null;
  cu: number | null;
  fe: number | null;
  mn: number | null;
  zn: number | null;

  // Titulação
  al: number | null;
  h_al: number | null;

  // Granulometria
  areia: number | null;
  argila: number | null;
  silte: number | null;

  // Calculados pelo backend (read-only)
  sb: number | null;
  t: number | null;
  T_maiusculo: number | null;
  V: number | null;
  m: number | null;
  ca_mg: number | null;
  ca_k: number | null;
  mg_k: number | null;
  c_org: number | null;
}

// ─── LeituraEquipamento (bancada) ─────────────────────────────────────────────

/** Leitura bruta de um elemento registrada na bancada, com resultado calculado. */
export interface LeituraDetalhe {
  id: number;
  bateria: number;
  elemento: string; // ex: "Ca", "Mg", "K"
  elemento_display: string; // ex: "Cálcio", "Magnésio"
  equipamento: string; // ex: "AA", "FC"
  leitura_bruta: number;
  fator_diluicao: number | null;
  resultado_calculado: number | null;
}

export type LeituraCorrecaoPayload = {
  leitura_bruta: number;
  fator_diluicao?: number | null;
};

/** Campos calculados — nunca enviados no payload. */
type CamposCalculados =
  | "id"
  | "laudo_id"
  | "sb"
  | "t"
  | "T_maiusculo"
  | "V"
  | "m"
  | "ca_mg"
  | "ca_k"
  | "mg_k"
  | "c_org";

export type AnaliseSoloPayload = Omit<AnaliseSolo, CamposCalculados>;

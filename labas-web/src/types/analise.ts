import type { Cliente } from "./cliente";

/**
 * Representa uma análise de solo completa, espelhando o model `AnaliseSolo` do Django.
 *
 * Campos agrupados por equipamento de origem:
 * - pH-metro: ph_agua, ph_cacl2, ph_kcl
 * - Espectrofotômetro: p_m, p_r, p_rem, mo, s, b
 * - Fotômetro de Chama: k, na
 * - Absorção Atômica: ca, mg, cu, fe, mn, zn
 * - Titulação: al, h_al
 * - Granulometria: areia, argila, silte
 *
 * Campos calculados automaticamente pelo backend (somente leitura no frontend):
 * sb, t, T_maiusculo, V, m, ca_mg, ca_k, mg_k, c_org
 */
export interface AnaliseSolo {
  /** Identificador do laudo no formato "ANO/NNN" — ex: "2026/001" */
  n_lab: string;

  /** Cliente (produtor rural) vinculado à amostra */
  cliente: Cliente;

  /** Data de entrada da amostra no laboratório (formato ISO: "YYYY-MM-DD") */
  data_entrada: string;

  /** Data de conclusão do laudo. Null enquanto ainda em análise */
  data_saida: string | null;

  // ─── pH-metro ────────────────────────────────────────────────────────────────

  /** pH em água */
  ph_agua: number | null;

  /** pH em solução de CaCl₂ */
  ph_cacl2: number | null;

  /** pH em solução de KCl */
  ph_kcl: number | null;

  // ─── Espectrofotômetro ────────────────────────────────────────────────────────

  /** Fósforo extraído pelo método Mehlich (mg/dm³) */
  p_m: number | null;

  /** Fósforo extraído pelo método Resina (mg/dm³) */
  p_r: number | null;

  /** Fósforo Remanescente — indica capacidade de adsorção do solo (mg/L) */
  p_rem: number | null;

  /** Matéria Orgânica (g/kg) */
  mo: number | null;

  /** Enxofre (mg/dm³) */
  s: number | null;

  /** Boro (mg/dm³) */
  b: number | null;

  // ─── Fotômetro de Chama ───────────────────────────────────────────────────────

  /** Potássio (cmolc/dm³) */
  k: number | null;

  /** Sódio (mg/dm³) */
  na: number | null;

  // ─── Absorção Atômica ─────────────────────────────────────────────────────────

  /** Cálcio (cmolc/dm³) */
  ca: number | null;

  /** Magnésio (cmolc/dm³) */
  mg: number | null;

  /** Cobre (mg/dm³) */
  cu: number | null;

  /** Ferro (mg/dm³) */
  fe: number | null;

  /** Manganês (mg/dm³) */
  mn: number | null;

  /** Zinco (mg/dm³) */
  zn: number | null;

  // ─── Titulação ────────────────────────────────────────────────────────────────

  /** Alumínio trocável (cmolc/dm³) */
  al: number | null;

  /** Acidez Potencial — Hidrogênio + Alumínio (cmolc/dm³) */
  h_al: number | null;

  // ─── Granulometria ────────────────────────────────────────────────────────────

  /** Areia (g/kg) */
  areia: number | null;

  /** Argila (g/kg) */
  argila: number | null;

  /** Silte (g/kg) */
  silte: number | null;

  // ─── Calculados pelo backend (read-only no frontend) ─────────────────────────

  /** Soma de Bases: Ca + Mg + K + Na (cmolc/dm³) */
  sb: number | null;

  /** CTC Efetiva: SB + Al (cmolc/dm³) */
  t: number | null;

  /** CTC a pH 7,0: SB + H+Al (cmolc/dm³) */
  T_maiusculo: number | null;

  /** Saturação por Bases: (SB / T) × 100 (%) */
  V: number | null;

  /** Saturação por Alumínio: (Al / t) × 100 (%) */
  m: number | null;

  /** Relação Ca/Mg */
  ca_mg: number | null;

  /** Relação Ca/K */
  ca_k: number | null;

  /** Relação Mg/K */
  mg_k: number | null;

  /** Carbono Orgânico (g/kg) */
  c_org: number | null;
}

/**
 * Payload para criação e edição de laudos via API.
 *
 * Remove os campos calculados pelo backend (somente leitura) e
 * substitui o objeto `cliente` pelo código do cliente (`cliente_codigo`),
 * conforme esperado pelo serializer do Django.
 */
export type AnaliseSoloPayload = Omit<
  AnaliseSolo,
  | "cliente"
  | "sb"
  | "t"
  | "T_maiusculo"
  | "V"
  | "m"
  | "ca_mg"
  | "ca_k"
  | "mg_k"
  | "c_org"
> & {
  /** Código do cliente — substitui o objeto `cliente` no payload de envio */
  cliente_codigo: string;
};

/** Resposta paginada padrão do DRF. */
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface PadraoLaboratorio {
  id: number;
  tipo: "padrao_a" | "padrao_b" | "p_labas_a" | "p_labas_b";
  tipo_display: string;
  ph_agua: number | null;
  ph_cacl2: number | null;
  ph_kcl: number | null;
  p_m: number | null;
  p_r: number | null;
  p_rem: number | null;
  mo: number | null;
  s: number | null;
  b: number | null;
  k: number | null;
  na: number | null;
  ca: number | null;
  mg: number | null;
  cu: number | null;
  fe: number | null;
  mn: number | null;
  zn: number | null;
  al: number | null;
  h_al: number | null;
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

export interface ConjuntoPadrao {
  id: number;
  nome: string;
  ativo: boolean;
  criado_em: string;
  atualizado_em: string;
  padroes: PadraoLaboratorio[];
}

export type PadraoPayload = Omit<PadraoLaboratorio, "id" | "tipo" | "tipo_display">;

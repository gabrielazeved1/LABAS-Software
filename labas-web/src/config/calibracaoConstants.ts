import type { Equipamento, Elemento } from "../types/calibracao";

export const EQUIPAMENTOS: { value: Equipamento; label: string }[] = [
  { value: "AA", label: "Absorção Atômica" },
  { value: "FC", label: "Fotômetro de Chama" },
  { value: "ES", label: "Espectrofotômetro" },
  { value: "TI", label: "Titulação" },
  { value: "PH", label: "pH-metro" },
];

export const ELEMENTOS: Elemento[] = [
  "Ca",
  "Mg",
  "Cu",
  "Fe",
  "Mn",
  "Zn",
  "K",
  "Na",
  "P_M",
  "P_R",
  "P_rem",
  "S",
  "B",
  "Al",
  "H_Al",
  "ph_agua",
  "ph_cacl2",
  "ph_kcl",
  "MO",
];

export const CALIBRACAO_STEPS = ["Dados da Bateria", "Pontos de Calibração"];

/** Equipamentos que exigem volume_solo e volume_extrator */
export const REQUER_VOLUMES: Equipamento[] = ["AA", "FC", "ES"];

/** Equipamentos que exigem leitura do branco */
export const REQUER_BRANCO: Equipamento[] = ["AA", "TI"];

/** Equipamentos que não utilizam curva de calibração (sem pontos concentração/leitura) */
export const SEM_CURVA_CALIBRACAO: Equipamento[] = ["TI", "PH"];

/** Label do campo de leitura instrumental por equipamento */
export const LEITURA_LABEL: Record<Equipamento, string> = {
  AA: "Absorvância",
  FC: "Emissão (u.a)",
  ES: "Transmitância (u.a)",
  TI: "Absorvância",
  PH: "Absorvância",
};

/** Elementos disponíveis por equipamento */
export const ELEMENTOS_POR_EQUIPAMENTO: Record<Equipamento, Elemento[]> = {
  AA: ["Ca", "Mg", "Cu", "Fe", "Mn", "Zn"],
  FC: ["K", "Na"],
  ES: ["P_M", "P_R", "P_rem", "S", "B", "MO"],
  TI: ["Al", "H_Al"],
  PH: ["ph_agua", "ph_cacl2", "ph_kcl"],
};

/** Labels de exibição para cada elemento */
export const ELEMENTO_LABEL: Record<Elemento, string> = {
  Ca: "Ca (Cálcio)",
  Mg: "Mg (Magnésio)",
  Cu: "Cu (Cobre)",
  Fe: "Fe (Ferro)",
  Mn: "Mn (Manganês)",
  Zn: "Zn (Zinco)",
  K: "K (Potássio)",
  Na: "Na (Sódio)",
  P_M: "P Mehlich",
  P_R: "P Resina",
  P_rem: "P Remanescente",
  S: "S (Enxofre)",
  B: "B (Boro)",
  Al: "Al (Alumínio)",
  H_Al: "H+Al (Acidez Potencial)",
  ph_agua: "pH Água",
  ph_cacl2: "pH CaCl₂",
  ph_kcl: "pH KCl",
  MO: "MO (Matéria Orgânica)",
};

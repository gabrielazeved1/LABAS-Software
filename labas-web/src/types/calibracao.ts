/**
 * Siglas dos equipamentos do laboratório.
 *
 * - AA: Absorção Atômica
 * - FC: Fotômetro de Chama
 * - ES: Espectrofotômetro
 * - TI: Titulação
 * - PH: pH-metro
 */
export type Equipamento = "AA" | "FC" | "ES" | "TI" | "PH";

/**
 * Elementos químicos que podem ser analisados em cada equipamento.
 * Espelha o campo `elemento` do model `BateriaCalibracao` no Django.
 */
export type Elemento =
  | "Ca"
  | "Mg"
  | "Cu"
  | "Fe"
  | "Mn"
  | "Zn"
  | "K"
  | "Na"
  | "P_M"
  | "P_R"
  | "P_rem"
  | "S"
  | "B"
  | "Al"
  | "H_Al"
  | "ph_agua"
  | "ph_cacl2"
  | "ph_kcl"
  | "MO";

/**
 * Representa uma bateria de calibração de um equipamento.
 *
 * Uma bateria agrupa os pontos de calibração de um único elemento
 * em um único equipamento para um determinado dia de análise.
 * A equação de regressão linear (y = ax + b) e o R² são calculados
 * automaticamente pelo backend conforme os pontos são adicionados.
 */
export interface BateriaCalibracao {
  id: number;

  /** Equipamento utilizado na bateria */
  equipamento: Equipamento;

  /** Elemento químico sendo calibrado */
  elemento: Elemento;

  /** Volume de solo utilizado no preparo da amostra (mL) */
  volume_solo: number | null;

  /** Volume do extrator utilizado no preparo da amostra (mL) */
  volume_extrator: number | null;

  /** Data e hora de criação da bateria (ISO 8601) */
  data_criacao: string;

  /** Coeficiente angular "a" da equação de regressão linear (y = ax + b) */
  coeficiente_angular_a: number | null;

  /** Coeficiente linear "b" da equação de regressão linear (y = ax + b) */
  coeficiente_linear_b: number | null;

  /** Coeficiente de determinação R² — qualidade do ajuste da curva (0 a 1) */
  r_quadrado: number | null;

  /** Leitura do branco (solução sem analito) para correção de fundo */
  leitura_branco: number | null;

  /** Indica se esta é a bateria ativa para o elemento/equipamento no dia */
  ativo: boolean;

  /**
   * Equação formatada gerada pelo backend — ex: "y = 0.4521x + 0.0031"
   * Campo read-only: nunca incluir em payloads de criação ou edição.
   */
  equacao_formada: string;
}

/**
 * Representa um ponto individual de calibração dentro de uma bateria.
 *
 * Cada ponto corresponde a um padrão de concentração conhecida
 * e sua respectiva leitura de absorvância no equipamento.
 * Com no mínimo 2 pontos, o backend calcula a regressão linear.
 */
export interface PontoCalibracao {
  id: number;

  /** ID da bateria à qual este ponto pertence */
  bateria: number;

  /** Concentração conhecida do padrão (mg/L ou cmolc/dm³, conforme elemento) */
  concentracao: number;

  /** Leitura de absorvância medida pelo equipamento para este padrão */
  absorvancia: number;
}

/**
 * Representa a leitura bruta de uma amostra real registrada em uma bateria ativa.
 *
 * A concentração real da amostra é calculada pelo backend
 * aplicando a equação da bateria sobre a leitura bruta,
 * com ajuste pelo fator de diluição quando aplicável.
 */
export interface LeituraEquipamento {
  id: number;

  /** ID da bateria ativa utilizada para calcular a concentração */
  bateria: number;

  /** Valor bruto lido diretamente pelo equipamento */
  leitura_bruta: number;

  /** Fator de diluição aplicado à amostra (1 = sem diluição) */
  fator_diluicao: number | null;
}

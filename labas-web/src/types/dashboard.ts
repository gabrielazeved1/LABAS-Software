// ─── KPIs agregados do laboratório ───────────────────────────────────────────

export interface DashboardStats {
  total_laudos: number;
  laudos_mes: number;
  total_amostras: number;
  amostras_mes: number;
  total_clientes: number;
  baterias_ativas: number;
}

// ─── Resumo de laudo para tabela de recentes ─────────────────────────────────

export interface LaudoResumo {
  id: number;
  codigo_laudo: string;
  cliente_nome: string;
  data_emissao: string;
  total_analises: number;
}

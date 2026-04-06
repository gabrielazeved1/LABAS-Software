/** Representa um cliente (Produtor Rural) conforme o model Django. */
export interface Cliente {
  codigo: string;
  nome: string;
  contato: string | null;
  municipio: string | null;
  area: string | null;
  observacoes: string | null;
}

/** Payload para criar ou atualizar um cliente via API (staff only). */
export type ClientePayload = {
  codigo: string;
  nome: string;
  contato?: string;
  municipio?: string;
  area?: string;
  observacoes?: string;
};

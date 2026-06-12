/** Representa um cliente (Produtor Rural) conforme o model Django. */
export interface Cliente {
  codigo: string;
  nome: string;
  email: string | null; // Separado para a automação de envio de Laudos
  telefone: string | null; // Separado para o link do WhatsApp
  municipio: string | null;
  area: string | null;
  observacoes: string | null;
}

/** Payload para criar ou atualizar um cliente via API (staff only). */
export type ClientePayload = {
  codigo: string;
  nome: string;
  email?: string;
  telefone?: string;
  municipio?: string;
  area?: string;
  observacoes?: string;
};

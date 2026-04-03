// src/services/clienteService.ts
import { api } from "./api";
import type { Cliente } from "../types/cliente";

/**
 * Serviço de acesso à API de clientes.
 *
 * Usado principalmente no Autocomplete do formulário de laudo
 * para que o staff selecione o cliente ao criar uma análise.
 *
 * Endpoint: GET /api/clientes/?search=<termo>
 */
export const clienteService = {
  /**
   * Lista clientes com suporte a busca por nome ou código.
   * @param search - Termo de busca (opcional). Filtra por nome ou código_cliente.
   */
  listar: (search?: string) =>
    api.get<Cliente[]>("/clientes/", {
      params: search ? { search } : undefined,
    }),

  /**
   * Busca um cliente específico pelo código.
   * @param codigo - Código único do cliente (ex: "2026-001")
   */
  buscar: (codigo: string) => api.get<Cliente>(`/clientes/${codigo}/`),
};

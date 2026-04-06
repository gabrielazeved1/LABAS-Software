// src/services/clienteService.ts
import { api } from "./api";
import type { Cliente, ClientePayload } from "../types/cliente";

export const clienteService = {
  /** Lista clientes. Suporta filtro por ?search= (nome ou código). */
  listar: async (search?: string): Promise<Cliente[]> => {
    const { data } = await api.get<Cliente[] | { results: Cliente[] }>(
      "/clientes/",
      {
        params: search ? { search } : undefined,
      },
    );
    return Array.isArray(data) ? data : data.results;
  },

  /** Busca um cliente pelo código. */
  buscar: async (codigo: string): Promise<Cliente> => {
    const { data } = await api.get<Cliente>(`/clientes/${codigo}/`);
    return data;
  },

  /** Cria um novo cliente (staff only). */
  criar: async (payload: ClientePayload): Promise<Cliente> => {
    const { data } = await api.post<Cliente>("/clientes/", payload);
    return data;
  },

  /** Atualiza parcialmente um cliente (staff only). */
  atualizar: async (
    codigo: string,
    payload: Partial<ClientePayload>,
  ): Promise<Cliente> => {
    const { data } = await api.patch<Cliente>(`/clientes/${codigo}/`, payload);
    return data;
  },

  /** Remove um cliente (staff only). */
  remover: async (codigo: string): Promise<void> => {
    await api.delete(`/clientes/${codigo}/`);
  },
};

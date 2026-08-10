// src/hooks/useClientes.ts
import { useState, useCallback, useRef } from "react";
import { clienteService } from "../services/clienteService";
import { useSnackbar } from "./useSnackbar";
import type { Cliente } from "../types/cliente";

interface UseClientesReturn {
  /** Lista de clientes retornada pela última busca */
  clientes: Cliente[];
  /** `true` enquanto a requisição está em andamento */
  loading: boolean;
  /**
   * Busca clientes por nome ou código.
   * Chamada a cada keystroke do Autocomplete — não faz debounce interno,
   * aplique debounce no componente se necessário.
   */
  buscar: (search: string) => Promise<void>;
  /** Limpa a lista de resultados */
  limpar: () => void;
}

/**
 * Hook para busca de clientes — alimenta o Autocomplete do LaudoFormPage.
 *
 * Responsabilidades:
 * - Manter a lista de resultados e o estado de loading
 * - Delegar a chamada HTTP ao clienteService
 * - Exibir erros via Snackbar sem expor detalhes ao componente
 *
 * @example
 * const { clientes, loading, buscar } = useClientes();
 *
 * <Autocomplete
 *   options={clientes}
 *   loading={loading}
 *   onInputChange={(_, value) => buscar(value)}
 *   getOptionLabel={(c) => `${c.codigo} — ${c.nome}`}
 * />
 */
export function useClientes(): UseClientesReturn {
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [loading, setLoading] = useState(false);
  const { showApiError } = useSnackbar();
  const controllerRef = useRef<AbortController | null>(null);

  const buscar = useCallback(
    async (search: string) => {
      // Cancela requisição anterior em voo
      controllerRef.current?.abort();

      if (search.trim().length < 2) {
        setClientes([]);
        return;
      }

      const controller = new AbortController();
      controllerRef.current = controller;

      setLoading(true);
      try {
        const resultado = await clienteService.listar(search, controller.signal);
        setClientes(resultado);
      } catch (err) {
        if ((err as { code?: string })?.code === "ERR_CANCELED") return;
        showApiError(err);
        setClientes([]);
      } finally {
        setLoading(false);
      }
    },
    [showApiError],
  );

  const limpar = useCallback(() => setClientes([]), []);

  return { clientes, loading, buscar, limpar };
}

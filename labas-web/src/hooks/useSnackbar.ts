// src/hooks/useSnackbar.ts
import { useContext } from "react";
import { SnackbarContext } from "../contexts/SnackbarContext";

/**
 * Hook para exibir notificações globais do LABAS.
 *
 * Deve ser usado em qualquer componente ou hook que precise dar feedback
 * ao usuário — nunca use Alert ou Snackbar diretamente nos componentes.
 *
 * @example
 * const { showSuccess, showApiError } = useSnackbar();
 *
 * try {
 *   await laudoService.criar(dados);
 *   showSuccess("Laudo criado com sucesso!");
 * } catch (err) {
 *   showApiError(err); // extrai e formata o erro do Django automaticamente
 * }
 */
export function useSnackbar() {
  const ctx = useContext(SnackbarContext);
  if (!ctx) {
    throw new Error("useSnackbar deve ser usado dentro de <SnackbarProvider>");
  }
  return ctx;
}

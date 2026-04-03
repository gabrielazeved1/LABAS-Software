/**
 * Hook de conveniência para consumir o {@link AuthContext} em qualquer componente.
 *
 * Por que um hook separado? (SOLID — S / DRY)
 * - Centraliza a guarda de null: qualquer componente fora do `<AuthProvider>`
 *   recebe um erro claro em tempo de desenvolvimento, em vez de falhar silenciosamente.
 * - Evita importar `useContext` + `AuthContext` em cada arquivo consumidor.
 *
 * @example
 * ```tsx
 * const { user, login, logout, isAuthenticated } = useAuth();
 * ```
 */

import { useContext } from "react";
import { AuthContext, type AuthContextValue } from "../contexts/AuthContext";

/**
 * Retorna o valor do {@link AuthContext}.
 *
 * @throws {Error} Se chamado fora de um `<AuthProvider>`.
 */
export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);

  if (!ctx) {
    throw new Error("useAuth deve ser chamado dentro de <AuthProvider>.");
  }

  return ctx;
}

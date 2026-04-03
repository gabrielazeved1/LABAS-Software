/**
 * Contexto global de autenticação do LABAS.
 *
 * Responsabilidades (SOLID — S):
 * - Manter o estado do usuário autenticado em memória.
 * - Persistir/limpar tokens JWT no localStorage.
 * - Restaurar a sessão ao recarregar a página (via `authService.me()`).
 * - Expor `login()` e `logout()` para qualquer componente da árvore.
 *
 * Este contexto NÃO faz chamadas HTTP diretamente — delega ao `authService`.
 * Redirecionamentos também ficam aqui, mantendo as páginas desacopladas de lógica de sessão.
 */

import {
  createContext,
  useState,
  useEffect,
  useCallback,
  type ReactNode,
} from "react";
import { useNavigate } from "react-router-dom";
import { authService } from "../services/authService";
import type { AuthUser, LoginPayload } from "../types/auth";

// ---------------------------------------------------------------------------
// Contrato do contexto
// ---------------------------------------------------------------------------

/**
 * Interface pública do AuthContext.
 *
 * Todos os componentes que consomem `useAuth()` enxergam exatamente estes campos.
 */
export interface AuthContextValue {
  /** Dados do usuário autenticado. `null` enquanto não autenticado ou durante o carregamento inicial. */
  user: AuthUser | null;
  /** `true` quando há um usuário autenticado em memória. */
  isAuthenticated: boolean;
  /** `true` quando o usuário autenticado possui permissão de staff (técnico/admin). */
  isStaff: boolean;
  /** `true` durante a verificação inicial de sessão (evita flash de tela de login). */
  loading: boolean;
  /**
   * Autentica o usuário com username e password.
   * Armazena os tokens JWT no localStorage e atualiza o estado interno.
   *
   * @throws Propaga o erro da API para que a camada de UI possa exibir feedback.
   */
  login: (data: LoginPayload) => Promise<void>;
  /**
   * Encerra a sessão do usuário.
   * Remove os tokens do localStorage, limpa o estado e redireciona para `/login`.
   */
  logout: () => void;
}

// ---------------------------------------------------------------------------
// Criação do contexto
// ---------------------------------------------------------------------------

/**
 * O valor `null` como default sinaliza que o hook `useAuth` foi chamado
 * fora de um `<AuthProvider>`. O hook lança um erro nesse caso.
 */
export const AuthContext = createContext<AuthContextValue | null>(null);

// ---------------------------------------------------------------------------
// Provider
// ---------------------------------------------------------------------------

interface AuthProviderProps {
  children: ReactNode;
}

/**
 * Provedor de autenticação. Deve envolver toda a árvore de rotas da aplicação.
 *
 * @example
 * ```tsx
 * // main.tsx
 * <BrowserRouter>
 *   <AuthProvider>
 *     <App />
 *   </AuthProvider>
 * </BrowserRouter>
 * ```
 */
export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  // -------------------------------------------------------------------------
  // Restauração de sessão na montagem do componente
  // -------------------------------------------------------------------------

  useEffect(() => {
    /**
     * Se há um access token salvo, tenta buscar os dados do usuário na API.
     * Isso garante que, ao recarregar a página, o usuário continue logado
     * sem precisar passar pelo fluxo de login novamente.
     *
     * Se o token estiver expirado, o interceptor de `api.ts` tentará fazer
     * o refresh automaticamente. Caso o refresh também falhe, o interceptor
     * limpa o localStorage — neste ponto `authService.me()` rejeita a Promise
     * e o usuário fica com `user = null` (não autenticado).
     */
    const restoreSession = async () => {
      const token = localStorage.getItem("access_token");

      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const response = await authService.me();
        setUser(response.data);
      } catch {
        // Token inválido ou expirado sem refresh disponível — sessão encerrada.
        // O interceptor de `api.ts` já limpa o localStorage nesse caminho.
      } finally {
        setLoading(false);
      }
    };

    restoreSession();
  }, []);

  // -------------------------------------------------------------------------
  // Listener para logout forçado pelo interceptor (refresh token expirado)
  // -------------------------------------------------------------------------

  useEffect(() => {
    const handleForceLogout = () => {
      setUser(null);
      navigate("/login", { replace: true });
    };

    window.addEventListener("labas:logout", handleForceLogout);
    return () => window.removeEventListener("labas:logout", handleForceLogout);
  }, [navigate]);

  // -------------------------------------------------------------------------
  // Ações expostas
  // -------------------------------------------------------------------------

  /**
   * Realiza o login: chama a API, persiste os tokens e atualiza o estado.
   * `useCallback` evita recriação desnecessária da função em cada render.
   */
  const login = useCallback(async (data: LoginPayload) => {
    const response = await authService.login(data);
    const { access, refresh } = response.data;

    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);

    // Busca os dados completos do usuário para popular o estado.
    const meResponse = await authService.me();
    setUser(meResponse.data);
  }, []);

  /**
   * Encerra a sessão: limpa o localStorage, zera o estado e redireciona.
   */
  const logout = useCallback(() => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUser(null);
    navigate("/login", { replace: true });
  }, [navigate]);

  // -------------------------------------------------------------------------
  // Valores derivados
  // -------------------------------------------------------------------------

  const isAuthenticated = user !== null;
  const isStaff = user?.is_staff ?? false;

  // -------------------------------------------------------------------------
  // Render
  // -------------------------------------------------------------------------

  const contextValue: AuthContextValue = {
    user,
    isAuthenticated,
    isStaff,
    loading,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  );
}

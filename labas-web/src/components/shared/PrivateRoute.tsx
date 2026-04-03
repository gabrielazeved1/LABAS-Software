// src/components/shared/PrivateRoute.tsx
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";

/**
 * Protege rotas que exigem autenticação.
 *
 * - Enquanto a sessão está sendo verificada (loading), não renderiza nada
 *   para evitar flash de redirecionamento.
 * - Usuário não autenticado é redirecionado para `/login`.
 * - Usuário autenticado renderiza a rota filho via <Outlet />.
 */
export default function PrivateRoute() {
  const { isAuthenticated, loading } = useAuth();

  if (loading) return null;

  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
}

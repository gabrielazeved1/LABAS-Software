// src/components/shared/StaffRoute.tsx
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";

/**
 * Protege rotas exclusivas de staff (técnicos/admins).
 *
 * - Enquanto a sessão está sendo verificada (loading), não renderiza nada.
 * - Usuário não autenticado é redirecionado para `/login`.
 * - Usuário autenticado mas sem permissão de staff é redirecionado para `/dashboard`.
 * - Staff autenticado renderiza a rota filho via <Outlet />.
 */
export default function StaffRoute() {
  const { isAuthenticated, isStaff, loading } = useAuth();

  if (loading) return null;

  if (!isAuthenticated) return <Navigate to="/login" replace />;

  return isStaff ? <Outlet /> : <Navigate to="/dashboard" replace />;
}

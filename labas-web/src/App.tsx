// src/App.tsx
import { Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/auth/LoginPage";
import RegisterPage from "./pages/auth/RegisterPage";
import DashboardPlaceholder from "./pages/dashboard/DashboardPlaceholder";
import PrivateRoute from "./components/shared/PrivateRoute";
import StaffRoute from "./components/shared/StaffRoute";
import AppShell from "./components/layout/AppShell";

export default function App() {
  return (
    <Routes>
      {/* Rotas públicas */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      {/* Rotas protegidas — qualquer usuário autenticado */}
      <Route element={<PrivateRoute />}>
        <Route
          path="/dashboard"
          element={
            <AppShell>
              <DashboardPlaceholder />
            </AppShell>
          }
        />
      </Route>

      {/* Rotas protegidas — apenas staff */}
      <Route element={<StaffRoute />}>
        {/* ex:
        <Route path="/calibracao" element={<AppShell><CalibracaoListPage /></AppShell>} />
        */}
      </Route>

      {/* Redireciona rota raiz para login por padrão */}
      <Route path="/" element={<Navigate to="/login" replace />} />
      {/* Fallback para rotas não encontradas */}
      <Route path="*" element={<h1>404 - Página não encontrada</h1>} />
    </Routes>
  );
}

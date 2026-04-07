// src/App.tsx
import { Routes, Route, Navigate } from "react-router-dom";
import { lazy, Suspense } from "react";
import LoginPage from "./pages/auth/LoginPage";
import RegisterPage from "./pages/auth/RegisterPage";
import DashboardPlaceholder from "./pages/dashboard/DashboardPlaceholder";
import PrivateRoute from "./components/shared/PrivateRoute";
import StaffRoute from "./components/shared/StaffRoute";
import AppShell from "./components/layout/AppShell";
import CircularProgress from "@mui/material/CircularProgress";
import Box from "@mui/material/Box";
import LaudosListPage from "./pages/laudos/LaudosListPage";

const CalibracaoListPage = lazy(
  () => import("./pages/calibracao/CalibracaoListPage"),
);
const CalibracaoFormPage = lazy(
  () => import("./pages/calibracao/CalibracaoFormPage"),
);

const Spinner = () => (
  <Box display="flex" justifyContent="center" py={8}>
    <CircularProgress />
  </Box>
);

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
        <Route
          path="/laudos"
          element={
            <AppShell>
              <LaudosListPage />
            </AppShell>
          }
        />
      </Route>

      {/* Rotas protegidas — apenas staff */}
      <Route element={<StaffRoute />}>
        <Route
          path="/calibracao"
          element={
            <AppShell>
              <Suspense fallback={<Spinner />}>
                <CalibracaoListPage />
              </Suspense>
            </AppShell>
          }
        />
        <Route
          path="/calibracao/nova"
          element={
            <AppShell>
              <Suspense fallback={<Spinner />}>
                <CalibracaoFormPage />
              </Suspense>
            </AppShell>
          }
        />
        <Route
          path="/calibracao/:id"
          element={
            <AppShell>
              <Suspense fallback={<Spinner />}>
                <CalibracaoFormPage />
              </Suspense>
            </AppShell>
          }
        />
      </Route>

      {/* Redireciona rota raiz para login por padrão */}
      <Route path="/" element={<Navigate to="/login" replace />} />
      {/* Fallback para rotas não encontradas */}
      <Route path="*" element={<h1>404 - Página não encontrada</h1>} />
    </Routes>
  );
}

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

const CalibracaoListPage = lazy(
  () => import("./pages/calibracao/CalibracaoListPage"),
);
const CalibracaoFormPage = lazy(
  () => import("./pages/calibracao/CalibracaoFormPage"),
);
const EntradaLotePage = lazy(
  () => import("./pages/operacao-lote/EntradaLotePage"),
);
const LaudoFormPage = lazy(() => import("./pages/laudos/LaudoFormPage"));
const LaudoEditPage = lazy(() => import("./pages/laudos/LaudoEditPage"));
const LaudosPage = lazy(() => import("./pages/laudos/LaudosPage"));
const ClientesPage = lazy(() => import("./pages/clientes/ClientesPage"));
const ClienteFormPage = lazy(() => import("./pages/clientes/ClienteFormPage"));

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
              <Suspense fallback={<Spinner />}>
                <LaudosPage />
              </Suspense>
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
        <Route
          path="/entrada-lote"
          element={
            <AppShell>
              <Suspense fallback={<Spinner />}>
                <EntradaLotePage />
              </Suspense>
            </AppShell>
          }
        />
        <Route
          path="/laudos/novo"
          element={
            <AppShell>
              <Suspense fallback={<Spinner />}>
                <LaudoFormPage />
              </Suspense>
            </AppShell>
          }
        />
        <Route
          path="/laudos/:nLab/editar"
          element={
            <AppShell>
              <Suspense fallback={<Spinner />}>
                <LaudoEditPage />
              </Suspense>
            </AppShell>
          }
        />
        <Route
          path="/clientes"
          element={
            <AppShell>
              <Suspense fallback={<Spinner />}>
                <ClientesPage />
              </Suspense>
            </AppShell>
          }
        />
        <Route
          path="/clientes/novo"
          element={
            <AppShell>
              <Suspense fallback={<Spinner />}>
                <ClienteFormPage />
              </Suspense>
            </AppShell>
          }
        />
        <Route
          path="/clientes/:codigo/editar"
          element={
            <AppShell>
              <Suspense fallback={<Spinner />}>
                <ClienteFormPage />
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

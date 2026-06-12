import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { Routes, Route } from "react-router-dom";
import StaffRoute from "../../components/shared/StaffRoute";
import { TestWrapper } from "../../test/TestWrapper";

/**
 * Renderiza o StaffRoute dentro de uma estrutura de rotas real.
 * A rota "/" é o filho protegido. "/login" e "/dashboard" são os destinos de redirecionamento.
 */
function renderStaffRoute(authValue = {}) {
  return render(
    <TestWrapper authValue={authValue} initialPath="/">
      <Routes>
        <Route element={<StaffRoute />}>
          <Route path="/" element={<div>Área Staff</div>} />
        </Route>
        <Route path="/login" element={<div>Página de Login</div>} />
        <Route path="/dashboard" element={<div>Dashboard</div>} />
      </Routes>
    </TestWrapper>,
  );
}

describe("StaffRoute", () => {
  it("não renderiza nada enquanto loading=true", () => {
    const { container } = renderStaffRoute({ loading: true });
    expect(container).toBeEmptyDOMElement();
  });

  it("redireciona para /login quando não autenticado", () => {
    renderStaffRoute({ isAuthenticated: false, loading: false });
    expect(screen.getByText("Página de Login")).toBeInTheDocument();
  });

  it("redireciona para /dashboard quando autenticado mas sem permissão de staff", () => {
    renderStaffRoute({
      isAuthenticated: true,
      isStaff: false,
      loading: false,
      user: {
        id: 2,
        username: "cliente",
        email: "cliente@ufubr",
        is_staff: false,
      },
    });
    expect(screen.getByText("Dashboard")).toBeInTheDocument();
  });

  it("renderiza a rota filha quando autenticado como staff", () => {
    renderStaffRoute({
      isAuthenticated: true,
      isStaff: true,
      loading: false,
      user: {
        id: 1,
        username: "gabriel",
        email: "gabriel@ufubr",
        is_staff: true,
      },
    });
    expect(screen.getByText("Área Staff")).toBeInTheDocument();
  });
});

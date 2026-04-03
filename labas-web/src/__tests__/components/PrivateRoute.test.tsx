import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { Routes, Route } from "react-router-dom";
import PrivateRoute from "../../components/shared/PrivateRoute";
import { TestWrapper } from "../../test/TestWrapper";

/**
 * Renderiza o PrivateRoute dentro de uma estrutura de rotas real.
 * A rota "/" é o filho protegido. "/login" é o destino do redirecionamento.
 */
function renderPrivateRoute(authValue = {}) {
  return render(
    <TestWrapper authValue={authValue} initialPath="/">
      <Routes>
        <Route element={<PrivateRoute />}>
          <Route path="/" element={<div>Área Protegida</div>} />
        </Route>
        <Route path="/login" element={<div>Página de Login</div>} />
      </Routes>
    </TestWrapper>,
  );
}

describe("PrivateRoute", () => {
  it("não renderiza nada enquanto loading=true", () => {
    const { container } = renderPrivateRoute({ loading: true });
    expect(container).toBeEmptyDOMElement();
  });

  it("redireciona para /login quando não autenticado", () => {
    renderPrivateRoute({ isAuthenticated: false, loading: false });
    expect(screen.getByText("Página de Login")).toBeInTheDocument();
  });

  it("renderiza a rota filha quando autenticado", () => {
    renderPrivateRoute({
      isAuthenticated: true,
      loading: false,
      user: {
        id: 1,
        username: "gabriel",
        email: "gabriel@ufubr",
        is_staff: false,
      },
    });
    expect(screen.getByText("Área Protegida")).toBeInTheDocument();
  });
});

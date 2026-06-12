import { describe, it, expect, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import LoginPage from "../../pages/auth/LoginPage";
import { TestWrapper } from "../../test/TestWrapper";

function renderLoginPage(loginFn = vi.fn()) {
  return render(
    <TestWrapper authValue={{ login: loginFn }}>
      <LoginPage />
    </TestWrapper>,
  );
}

describe("LoginPage", () => {
  it("renderiza os campos de usuário e senha", () => {
    renderLoginPage();
    expect(screen.getByLabelText(/usuário/i)).toBeInTheDocument();
    expect(
      screen.getByLabelText("Senha", { selector: "input" }),
    ).toBeInTheDocument();
  });

  it("renderiza o botão Entrar", () => {
    renderLoginPage();
    expect(screen.getByRole("button", { name: /entrar/i })).toBeInTheDocument();
  });

  it("exibe erro de validação quando campos estão vazios", async () => {
    renderLoginPage();
    const user = userEvent.setup();

    await user.click(screen.getByRole("button", { name: /entrar/i }));

    await waitFor(() => {
      expect(screen.getByText(/usuário é obrigatório/i)).toBeInTheDocument();
    });
  });

  it("exibe erro de validação para username muito curto", async () => {
    renderLoginPage();
    const user = userEvent.setup();

    await user.type(screen.getByLabelText(/usuário/i), "ab");
    await user.click(screen.getByRole("button", { name: /entrar/i }));

    await waitFor(() => {
      expect(screen.getByText(/mínimo de 3 caracteres/i)).toBeInTheDocument();
    });
  });

  it("chama loginFn com dados corretos ao submeter", async () => {
    const loginFn = vi.fn().mockResolvedValue(undefined);
    renderLoginPage(loginFn);
    const user = userEvent.setup();

    await user.type(screen.getByLabelText(/usuário/i), "joao123");
    await user.type(
      screen.getByLabelText("Senha", { selector: "input" }),
      "123456",
    );
    await user.click(screen.getByRole("button", { name: /entrar/i }));

    await waitFor(() => {
      expect(loginFn).toHaveBeenCalledWith({
        username: "joao123",
        password: "123456",
      });
    });
  });

  it("exibe mensagem de erro da API quando login falha", async () => {
    const loginFn = vi.fn().mockRejectedValue({
      response: { data: { detail: "Credenciais inválidas." } },
    });
    renderLoginPage(loginFn);
    const user = userEvent.setup();

    await user.type(screen.getByLabelText(/usuário/i), "joao123");
    await user.type(
      screen.getByLabelText("Senha", { selector: "input" }),
      "123456",
    );
    await user.click(screen.getByRole("button", { name: /entrar/i }));

    await waitFor(() => {
      expect(screen.getByText(/credenciais inválidas/i)).toBeInTheDocument();
    });
  });

  it("redireciona para /dashboard se já autenticado", () => {
    render(
      <TestWrapper authValue={{ isAuthenticated: true, loading: false }}>
        <LoginPage />
      </TestWrapper>,
    );
    // Navigate redireciona — o componente não renderiza o formulário
    expect(screen.queryByLabelText(/usuário/i)).not.toBeInTheDocument();
  });
});

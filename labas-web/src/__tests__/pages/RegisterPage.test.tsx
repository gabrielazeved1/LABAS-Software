import { describe, it, expect, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import RegisterPage from "../../pages/auth/RegisterPage";
import { TestWrapper } from "../../test/TestWrapper";
import * as authServiceModule from "../../services/authService";

function renderRegisterPage(loginFn = vi.fn()) {
  return render(
    <TestWrapper authValue={{ login: loginFn }} initialPath="/register">
      <RegisterPage />
    </TestWrapper>,
  );
}

describe("RegisterPage — Step 1 (Credenciais)", () => {
  it("renderiza os campos do step 1", () => {
    renderRegisterPage();
    expect(screen.getByLabelText(/usuário/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/e-mail/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^senha$/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/confirmar senha/i)).toBeInTheDocument();
  });

  it("exibe erros de validação do step 1 quando campos estão vazios", async () => {
    renderRegisterPage();
    const user = userEvent.setup();

    await user.click(screen.getByRole("button", { name: /próximo/i }));

    await waitFor(() => {
      expect(screen.getByText(/mínimo de 3 caracteres/i)).toBeInTheDocument();
    });
  });

  it("exibe erro quando e-mail é inválido", async () => {
    renderRegisterPage();
    const user = userEvent.setup();

    await user.type(screen.getByLabelText(/usuário/i), "joao123");
    await user.type(screen.getByLabelText(/e-mail/i), "nao-e-email");
    await user.type(screen.getByLabelText(/^senha$/i), "123456");
    await user.type(screen.getByLabelText(/confirmar senha/i), "123456");
    await user.click(screen.getByRole("button", { name: /próximo/i }));

    await waitFor(() => {
      expect(screen.getByText(/e-mail inválido/i)).toBeInTheDocument();
    });
  });

  it("exibe erro quando senhas não coincidem", async () => {
    renderRegisterPage();
    const user = userEvent.setup();

    await user.type(screen.getByLabelText(/usuário/i), "joao123");
    await user.type(screen.getByLabelText(/e-mail/i), "joao@example.com");
    await user.type(screen.getByLabelText(/^senha$/i), "123456");
    await user.type(screen.getByLabelText(/confirmar senha/i), "outra_senha");
    await user.click(screen.getByRole("button", { name: /próximo/i }));

    await waitFor(() => {
      expect(screen.getByText(/as senhas não coincidem/i)).toBeInTheDocument();
    });
  });

  it("avança para step 2 com dados válidos", async () => {
    renderRegisterPage();
    const user = userEvent.setup();

    await user.type(screen.getByLabelText(/usuário/i), "joao123");
    await user.type(screen.getByLabelText(/e-mail/i), "joao@example.com");
    await user.type(screen.getByLabelText(/^senha$/i), "123456");
    await user.type(screen.getByLabelText(/confirmar senha/i), "123456");
    await user.click(screen.getByRole("button", { name: /próximo/i }));

    await waitFor(() => {
      expect(screen.getByLabelText(/nome completo/i)).toBeInTheDocument();
    });
  });
});

describe("RegisterPage — Step 2 (Dados do cliente)", () => {
  async function avancarParaStep2() {
    const loginFn = vi.fn().mockResolvedValue(undefined);
    renderRegisterPage(loginFn);
    const user = userEvent.setup();

    await user.type(screen.getByLabelText(/usuário/i), "joao123");
    await user.type(screen.getByLabelText(/e-mail/i), "joao@example.com");
    await user.type(screen.getByLabelText(/^senha$/i), "123456");
    await user.type(screen.getByLabelText(/confirmar senha/i), "123456");
    await user.click(screen.getByRole("button", { name: /próximo/i }));

    await waitFor(() => {
      expect(screen.getByLabelText(/nome completo/i)).toBeInTheDocument();
    });

    return { user, loginFn };
  }

  it("exibe erro quando nome é muito curto", async () => {
    const { user } = await avancarParaStep2();

    await user.type(screen.getByLabelText(/nome completo/i), "ab");
    await user.type(screen.getByLabelText(/código do cliente/i), "1001");
    await user.click(screen.getByRole("button", { name: /criar conta/i }));

    await waitFor(() => {
      expect(screen.getByText(/nome é obrigatório/i)).toBeInTheDocument();
    });
  });

  it("exibe erro quando código tem letras", async () => {
    const { user } = await avancarParaStep2();

    await user.type(
      screen.getByLabelText(/nome completo/i),
      "Fazenda Boa Vista",
    );
    await user.type(screen.getByLabelText(/código do cliente/i), "ABC");
    await user.click(screen.getByRole("button", { name: /criar conta/i }));

    await waitFor(() => {
      expect(screen.getByText(/apenas números/i)).toBeInTheDocument();
    });
  });

  it("submete e chama register + login com dados corretos", async () => {
    const registerSpy = vi
      .spyOn(authServiceModule.authService, "register")
      .mockResolvedValue({ data: { message: "ok" } } as any);

    const { user, loginFn } = await avancarParaStep2();

    await user.type(
      screen.getByLabelText(/nome completo/i),
      "Fazenda Boa Vista",
    );
    await user.type(screen.getByLabelText(/código do cliente/i), "1001");
    await user.click(screen.getByRole("button", { name: /criar conta/i }));

    await waitFor(() => {
      expect(registerSpy).toHaveBeenCalledWith(
        expect.objectContaining({
          username: "joao123",
          nome_cliente: "Fazenda Boa Vista",
          codigo_cliente: "1001",
        }),
      );
    });

    await waitFor(() => {
      expect(loginFn).toHaveBeenCalledWith({
        username: "joao123",
        password: "123456",
      });
    });

    registerSpy.mockRestore();
  });

  it("exibe erro da API quando código já existe", async () => {
    vi.spyOn(authServiceModule.authService, "register").mockRejectedValue({
      response: {
        data: { codigo_cliente: ["Já existe um cliente com este código."] },
      },
    });

    const { user } = await avancarParaStep2();

    await user.type(
      screen.getByLabelText(/nome completo/i),
      "Fazenda Boa Vista",
    );
    await user.type(screen.getByLabelText(/código do cliente/i), "1001");
    await user.click(screen.getByRole("button", { name: /criar conta/i }));

    await waitFor(() => {
      expect(
        screen.getByText(/já existe um cliente com este código/i),
      ).toBeInTheDocument();
    });

    vi.restoreAllMocks();
  });
});

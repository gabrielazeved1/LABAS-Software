import { describe, it, expect } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { SnackbarProvider } from "../../contexts/SnackbarContext";
import { useSnackbar } from "../../hooks/useSnackbar";

// ---------------------------------------------------------------------------
// Componente auxiliar de teste
// ---------------------------------------------------------------------------

/**
 * Renderiza um botão que dispara o método do Snackbar recebido como prop.
 * Após o clique, o Snackbar deve aparecer com a mensagem esperada.
 */
function SnackbarTrigger({
  action,
}: {
  action: (ctx: ReturnType<typeof useSnackbar>) => void;
}) {
  const ctx = useSnackbar();
  return <button onClick={() => action(ctx)}>disparar</button>;
}

function renderWithSnackbar(
  action: (ctx: ReturnType<typeof useSnackbar>) => void,
) {
  return render(
    <SnackbarProvider>
      <SnackbarTrigger action={action} />
    </SnackbarProvider>,
  );
}

// ---------------------------------------------------------------------------
// Testes
// ---------------------------------------------------------------------------

describe("SnackbarContext — métodos diretos", () => {
  it("showSuccess exibe a mensagem com severidade success", async () => {
    renderWithSnackbar((ctx) => ctx.showSuccess("Operação realizada!"));
    await userEvent.click(screen.getByRole("button", { name: /disparar/i }));
    expect(screen.getByText("Operação realizada!")).toBeInTheDocument();
    expect(screen.getByRole("alert")).toHaveClass("MuiAlert-filledSuccess");
  });

  it("showError exibe a mensagem com severidade error", async () => {
    renderWithSnackbar((ctx) => ctx.showError("Algo deu errado."));
    await userEvent.click(screen.getByRole("button", { name: /disparar/i }));
    expect(screen.getByText("Algo deu errado.")).toBeInTheDocument();
    expect(screen.getByRole("alert")).toHaveClass("MuiAlert-filledError");
  });

  it("showWarning exibe a mensagem com severidade warning", async () => {
    renderWithSnackbar((ctx) => ctx.showWarning("Atenção!"));
    await userEvent.click(screen.getByRole("button", { name: /disparar/i }));
    expect(screen.getByText("Atenção!")).toBeInTheDocument();
    expect(screen.getByRole("alert")).toHaveClass("MuiAlert-filledWarning");
  });

  it("showInfo exibe a mensagem com severidade info", async () => {
    renderWithSnackbar((ctx) => ctx.showInfo("Informação adicional."));
    await userEvent.click(screen.getByRole("button", { name: /disparar/i }));
    expect(screen.getByText("Informação adicional.")).toBeInTheDocument();
    expect(screen.getByRole("alert")).toHaveClass("MuiAlert-filledInfo");
  });
});

describe("SnackbarContext — showApiError", () => {
  it("exibe `detail` quando o erro tem formato { detail: string } (403/404)", async () => {
    const error = { response: { data: { detail: "Você não tem permissão." } } };
    renderWithSnackbar((ctx) => ctx.showApiError(error));
    await userEvent.click(screen.getByRole("button", { name: /disparar/i }));
    expect(screen.getByText("Você não tem permissão.")).toBeInTheDocument();
  });

  it("exibe os campos quando o erro tem formato { campo: [msg] } (400 validação)", async () => {
    const error = {
      response: {
        data: {
          username: ["Este campo já existe."],
          email: ["Email inválido."],
        },
      },
    };
    renderWithSnackbar((ctx) => ctx.showApiError(error));
    await userEvent.click(screen.getByRole("button", { name: /disparar/i }));
    expect(
      screen.getByText(/username: Este campo já existe\./),
    ).toBeInTheDocument();
    expect(screen.getByText(/email: Email inválido\./)).toBeInTheDocument();
  });

  it("exibe mensagem genérica quando o erro não tem formato reconhecível", async () => {
    renderWithSnackbar((ctx) => ctx.showApiError(new Error("network error")));
    await userEvent.click(screen.getByRole("button", { name: /disparar/i }));
    expect(
      screen.getByText("Ocorreu um erro inesperado. Tente novamente."),
    ).toBeInTheDocument();
  });

  it("fecha o snackbar ao clicar no botão de fechar", async () => {
    renderWithSnackbar((ctx) => ctx.showSuccess("Fechável!"));
    await userEvent.click(screen.getByRole("button", { name: /disparar/i }));
    expect(screen.getByText("Fechável!")).toBeInTheDocument();

    // O Alert do MUI renderiza um botão com aria-label="Close"
    await userEvent.click(screen.getByRole("button", { name: /close/i }));

    // O MUI usa transição de saída (Fade) — o elemento permanece no DOM mas fica oculto
    await waitFor(() => {
      expect(screen.queryByText("Fechável!")).not.toBeVisible();
    });
  });
});

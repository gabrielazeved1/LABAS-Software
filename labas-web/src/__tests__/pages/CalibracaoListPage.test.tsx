import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import CalibracaoListPage from "../../pages/calibracao/CalibracaoListPage";
import { TestWrapper } from "../../test/TestWrapper";

vi.mock("../../hooks/useCalibracao", () => ({
  useCalibracao: vi.fn(),
}));

vi.mock("react-router-dom", async (importOriginal) => {
  const actual = await importOriginal<typeof import("react-router-dom")>();
  return { ...actual, useNavigate: vi.fn(() => vi.fn()) };
});

import { useCalibracao } from "../../hooks/useCalibracao";

const mockUseCalibracao = useCalibracao as ReturnType<typeof vi.fn>;

const bateriaFixture = {
  id: 1,
  equipamento: "AA",
  elemento: "Ca",
  volume_solo: 5,
  volume_extrator: 50,
  data_criacao: "2026-04-03T08:00:00Z",
  coeficiente_angular_a: 0.45,
  coeficiente_linear_b: 0.003,
  r_quadrado: 0.9987,
  leitura_branco: 0.002,
  ativo: true,
  equacao_formada: "y = 0.450000x + 0.003000",
  pontos: [],
};

const defaultHookReturn = {
  baterias: [bateriaFixture],
  loading: false,
  equipamentoFiltro: undefined,
  setEquipamentoFiltro: vi.fn(),
  criarBateria: vi.fn(),
  toggleAtivo: vi.fn(),
  removerBateria: vi.fn(),
  recarregar: vi.fn(),
};

function renderPage(
  authValue = {
    user: { id: 1, username: "tech", email: "t@t.com", is_staff: true },
    isAuthenticated: true,
    isStaff: true,
  },
) {
  return render(
    <TestWrapper authValue={authValue}>
      <CalibracaoListPage />
    </TestWrapper>,
  );
}

beforeEach(() => {
  vi.clearAllMocks();
  mockUseCalibracao.mockReturnValue(defaultHookReturn);
});

describe("CalibracaoListPage", () => {
  it("renderiza as tabs de equipamentos", () => {
    renderPage();
    expect(
      screen.getByRole("tab", { name: /Absorção Atômica/i }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("tab", { name: /Fotômetro de Chama/i }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("tab", { name: /Espectrofotômetro/i }),
    ).toBeInTheDocument();
    expect(screen.getByRole("tab", { name: /Titulação/i })).toBeInTheDocument();
    expect(screen.getByRole("tab", { name: /pH-metro/i })).toBeInTheDocument();
  });

  it("exibe baterias da aba ativa", () => {
    renderPage();
    expect(screen.getByText("Ca")).toBeInTheDocument();
    expect(screen.getByText("y = 0.450000x + 0.003000")).toBeInTheDocument();
  });

  it("exibe EmptyState quando não há baterias na aba", () => {
    mockUseCalibracao.mockReturnValue({ ...defaultHookReturn, baterias: [] });
    renderPage();
    expect(screen.getByText(/nenhuma bateria encontrada/i)).toBeInTheDocument();
  });

  it("exibe spinner enquanto loading=true", () => {
    mockUseCalibracao.mockReturnValue({ ...defaultHookReturn, loading: true });
    renderPage();
    expect(screen.getByRole("progressbar")).toBeInTheDocument();
  });

  it("Switch de ativo chama toggleAtivo com id e novo valor", async () => {
    const toggleAtivo = vi.fn();
    mockUseCalibracao.mockReturnValue({ ...defaultHookReturn, toggleAtivo });

    renderPage();
    const user = userEvent.setup();

    const switchEl = screen.getByRole("checkbox", {
      name: /ativar bateria 1/i,
    });
    await user.click(switchEl);

    expect(toggleAtivo).toHaveBeenCalledWith(1, false);
  });

  it("clicar em remover e confirmar chama removerBateria", async () => {
    const removerBateria = vi.fn().mockResolvedValue(undefined);
    mockUseCalibracao.mockReturnValue({ ...defaultHookReturn, removerBateria });

    renderPage();
    const user = userEvent.setup();

    await user.click(
      screen.getByRole("button", { name: /remover bateria 1/i }),
    );

    // Dialog de confirmação abre
    await waitFor(() => expect(screen.getByRole("dialog")).toBeInTheDocument());

    // Confirmar
    const dialog = screen.getByRole("dialog");
    await user.click(
      within(dialog).getByRole("button", {
        name: /confirmar|excluir|remover/i,
      }),
    );

    await waitFor(() => expect(removerBateria).toHaveBeenCalledWith(1));
  });
});

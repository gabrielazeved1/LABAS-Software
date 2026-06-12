import { describe, it, expect, vi, beforeEach } from "vitest";
import { calibracaoService } from "../../services/calibracaoService";
import { api } from "../../services/api";

vi.mock("../../services/api", () => ({
  api: {
    get: vi.fn(),
    post: vi.fn(),
    patch: vi.fn(),
    delete: vi.fn(),
  },
}));

const mockApi = api as unknown as {
  get: ReturnType<typeof vi.fn>;
  post: ReturnType<typeof vi.fn>;
  patch: ReturnType<typeof vi.fn>;
  delete: ReturnType<typeof vi.fn>;
};

const bateriaFixture = {
  id: 1,
  equipamento: "AA",
  elemento: "Ca",
  volume_solo: 5.0,
  volume_extrator: 50.0,
  data_criacao: "2026-04-03T08:00:00Z",
  coeficiente_angular_a: 0.4521,
  coeficiente_linear_b: 0.0031,
  r_quadrado: 0.9987,
  leitura_branco: 0.002,
  ativo: true,
  equacao_formada: "y = 0.452100x + 0.003100",
  pontos: [],
};

const pontoFixture = {
  id: 10,
  bateria: 1,
  concentracao: 2.5,
  absorvancia: 0.137,
};

beforeEach(() => {
  vi.clearAllMocks();
});

describe("calibracaoService.listarBaterias", () => {
  it("retorna array de baterias sem filtro", async () => {
    mockApi.get.mockResolvedValue({ data: [bateriaFixture] });

    const result = await calibracaoService.listarBaterias();

    expect(mockApi.get).toHaveBeenCalledWith("/baterias/", { params: {} });
    expect(result).toHaveLength(1);
    expect(result[0].elemento).toBe("Ca");
  });

  it("passa filtro de equipamento como query param", async () => {
    mockApi.get.mockResolvedValue({ data: [] });

    await calibracaoService.listarBaterias("FC");

    expect(mockApi.get).toHaveBeenCalledWith("/baterias/", {
      params: { equipamento: "FC" },
    });
  });
});

describe("calibracaoService.criarBateria", () => {
  it("envia o payload correto e retorna bateria criada", async () => {
    mockApi.post.mockResolvedValue({ data: bateriaFixture });

    const payload = {
      equipamento: "AA" as const,
      elemento: "Ca",
      volume_solo: 5.0,
      volume_extrator: 50.0,
      leitura_branco: 0.002,
    };

    const result = await calibracaoService.criarBateria(payload);

    expect(mockApi.post).toHaveBeenCalledWith("/baterias/", payload);
    expect(result.id).toBe(1);
    expect(result.equacao_formada).toBe("y = 0.452100x + 0.003100");
  });
});

describe("calibracaoService.toggleAtivo", () => {
  it("envia PATCH com { ativo: true } e retorna bateria atualizada", async () => {
    mockApi.patch.mockResolvedValue({
      data: { ...bateriaFixture, ativo: true },
    });

    const result = await calibracaoService.toggleAtivo(1, true);

    expect(mockApi.patch).toHaveBeenCalledWith("/baterias/1/", { ativo: true });
    expect(result.ativo).toBe(true);
  });

  it("envia PATCH com { ativo: false } para desativar", async () => {
    mockApi.patch.mockResolvedValue({
      data: { ...bateriaFixture, ativo: false },
    });

    await calibracaoService.toggleAtivo(1, false);

    expect(mockApi.patch).toHaveBeenCalledWith("/baterias/1/", {
      ativo: false,
    });
  });
});

describe("calibracaoService.adicionarPonto", () => {
  it("envia ponto no endpoint correto e retorna ponto criado", async () => {
    mockApi.post.mockResolvedValue({ data: pontoFixture });

    const result = await calibracaoService.adicionarPonto(1, {
      concentracao: 2.5,
      absorvancia: 0.137,
      bateria: 1,
    });

    expect(mockApi.post).toHaveBeenCalledWith("/baterias/1/pontos/", {
      concentracao: 2.5,
      absorvancia: 0.137,
      bateria: 1,
    });
    expect(result.id).toBe(10);
  });
});

describe("calibracaoService.removerPonto", () => {
  it("chama DELETE no endpoint correto do ponto", async () => {
    mockApi.delete.mockResolvedValue({ data: undefined });

    await calibracaoService.removerPonto(10);

    expect(mockApi.delete).toHaveBeenCalledWith("/pontos/10/");
  });
});

describe("calibracaoService.removerBateria", () => {
  it("chama DELETE no endpoint correto da bateria", async () => {
    mockApi.delete.mockResolvedValue({ data: undefined });

    await calibracaoService.removerBateria(1);

    expect(mockApi.delete).toHaveBeenCalledWith("/baterias/1/");
  });
});

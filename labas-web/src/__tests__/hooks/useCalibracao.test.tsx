import { describe, it, expect, vi, beforeEach } from "vitest";
import { renderHook, act, waitFor } from "@testing-library/react";
import { useCalibracao } from "../../hooks/useCalibracao";
import { useBateriaDetalhe } from "../../hooks/useBateriaDetalhe";
import * as calibracaoServiceModule from "../../services/calibracaoService";
import { TestWrapper } from "../../test/TestWrapper";
import type { ReactNode } from "react";

vi.mock("../../services/calibracaoService");

const mockedService =
  calibracaoServiceModule.calibracaoService as unknown as Record<
    string,
    ReturnType<typeof vi.fn>
  >;

const bateriaA = {
  id: 1,
  equipamento: "AA",
  elemento: "Ca",
  volume_solo: 5,
  volume_extrator: 50,
  data_criacao: "2026-04-03T08:00:00Z",
  coeficiente_angular_a: 0.45,
  coeficiente_linear_b: 0.003,
  r_quadrado: 0.998,
  leitura_branco: 0.002,
  ativo: true,
  equacao_formada: "y = 0.450000x + 0.003000",
  pontos: [],
};

const bateriaB = { ...bateriaA, id: 2, ativo: false };

const wrapper = ({ children }: { children: ReactNode }) => (
  <TestWrapper>{children}</TestWrapper>
);

beforeEach(() => {
  vi.clearAllMocks();
});

// ---------------------------------------------------------------------------
// useCalibracao
// ---------------------------------------------------------------------------

describe("useCalibracao", () => {
  it("carrega baterias ao montar", async () => {
    mockedService.listarBaterias = vi
      .fn()
      .mockResolvedValue([bateriaA, bateriaB]);

    const { result } = renderHook(() => useCalibracao(), { wrapper });

    await waitFor(() => expect(result.current.loading).toBe(false));

    expect(mockedService.listarBaterias).toHaveBeenCalledTimes(1);
    expect(result.current.baterias).toHaveLength(2);
  });

  it("recarrega com filtro quando equipamentoFiltro muda", async () => {
    mockedService.listarBaterias = vi.fn().mockResolvedValue([bateriaA]);

    const { result } = renderHook(() => useCalibracao(), { wrapper });

    await waitFor(() => expect(result.current.loading).toBe(false));

    act(() => {
      result.current.setEquipamentoFiltro("FC");
    });

    await waitFor(() =>
      expect(mockedService.listarBaterias).toHaveBeenCalledTimes(2),
    );
    expect(mockedService.listarBaterias).toHaveBeenLastCalledWith("FC");
  });

  it("toggleAtivo chama o service e faz refetch da lista", async () => {
    mockedService.listarBaterias = vi.fn().mockResolvedValue([bateriaA]);
    mockedService.toggleAtivo = vi
      .fn()
      .mockResolvedValue({ ...bateriaA, ativo: false });

    const { result } = renderHook(() => useCalibracao(), { wrapper });
    await waitFor(() => expect(result.current.loading).toBe(false));

    const listarCallsAntes = (
      mockedService.listarBaterias as ReturnType<typeof vi.fn>
    ).mock.calls.length;

    await act(async () => {
      await result.current.toggleAtivo(1, false);
    });

    expect(mockedService.toggleAtivo).toHaveBeenCalledWith(1, false);
    expect(
      (mockedService.listarBaterias as ReturnType<typeof vi.fn>).mock.calls
        .length,
    ).toBeGreaterThan(listarCallsAntes);
  });

  it("removerBateria chama o service e faz refetch", async () => {
    mockedService.listarBaterias = vi.fn().mockResolvedValue([bateriaA]);
    mockedService.removerBateria = vi.fn().mockResolvedValue(undefined);

    const { result } = renderHook(() => useCalibracao(), { wrapper });
    await waitFor(() => expect(result.current.loading).toBe(false));

    await act(async () => {
      await result.current.removerBateria(1);
    });

    expect(mockedService.removerBateria).toHaveBeenCalledWith(1);
  });
});

// ---------------------------------------------------------------------------
// useBateriaDetalhe
// ---------------------------------------------------------------------------

describe("useBateriaDetalhe", () => {
  const bateriaComPontos = {
    ...bateriaA,
    pontos: [{ id: 10, bateria: 1, concentracao: 2.5, absorvancia: 0.137 }],
  };

  it("carrega bateria com pontos ao receber id", async () => {
    mockedService.buscarBateria = vi.fn().mockResolvedValue(bateriaComPontos);

    const { result } = renderHook(() => useBateriaDetalhe(1), { wrapper });

    await waitFor(() => expect(result.current.loading).toBe(false));

    expect(mockedService.buscarBateria).toHaveBeenCalledWith(1);
    expect(result.current.bateria?.pontos).toHaveLength(1);
  });

  it("nao faz fetch quando id e null", async () => {
    mockedService.buscarBateria = vi.fn();

    renderHook(() => useBateriaDetalhe(null), { wrapper });

    await waitFor(() => new Promise((r) => setTimeout(r, 50)));

    expect(mockedService.buscarBateria).not.toHaveBeenCalled();
  });

  it("adicionarPonto chama service e recarrega bateria", async () => {
    mockedService.buscarBateria = vi.fn().mockResolvedValue(bateriaComPontos);
    mockedService.adicionarPonto = vi.fn().mockResolvedValue({
      id: 11,
      bateria: 1,
      concentracao: 5.0,
      absorvancia: 0.275,
    });

    const { result } = renderHook(() => useBateriaDetalhe(1), { wrapper });
    await waitFor(() => expect(result.current.loading).toBe(false));

    await act(async () => {
      await result.current.adicionarPonto({
        concentracao: 5.0,
        absorvancia: 0.275,
        bateria: 1,
      });
    });

    expect(mockedService.adicionarPonto).toHaveBeenCalledWith(1, {
      concentracao: 5.0,
      absorvancia: 0.275,
      bateria: 1,
    });
    expect(mockedService.buscarBateria).toHaveBeenCalledTimes(2);
  });

  it("removerPonto chama service e recarrega bateria", async () => {
    mockedService.buscarBateria = vi.fn().mockResolvedValue(bateriaComPontos);
    mockedService.removerPonto = vi.fn().mockResolvedValue(undefined);

    const { result } = renderHook(() => useBateriaDetalhe(1), { wrapper });
    await waitFor(() => expect(result.current.loading).toBe(false));

    await act(async () => {
      await result.current.removerPonto(10);
    });

    expect(mockedService.removerPonto).toHaveBeenCalledWith(10);
    expect(mockedService.buscarBateria).toHaveBeenCalledTimes(2);
  });
});

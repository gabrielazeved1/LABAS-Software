import { describe, it, expect, vi } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { useRegisterForm } from "../../hooks/useRegisterForm";

const step1 = {
  username: "joao123",
  email: "joao@example.com",
  password: "123456",
  password2: "123456",
};

const step2 = {
  nome_cliente: "Fazenda Boa Vista",
  codigo_cliente: "1001",
  municipio: "Uberlândia",
  area: "100",
};

describe("useRegisterForm", () => {
  it("inicia no step 0 sem erro", () => {
    const { result } = renderHook(() =>
      useRegisterForm(vi.fn(), vi.fn(), vi.fn()),
    );
    expect(result.current.activeStep).toBe(0);
    expect(result.current.apiError).toBeNull();
  });

  it("avança para step 1 ao submeter step 1 válido", () => {
    const { result } = renderHook(() =>
      useRegisterForm(vi.fn(), vi.fn(), vi.fn()),
    );

    act(() => {
      result.current.handleStep1Submit(step1);
    });

    expect(result.current.activeStep).toBe(1);
    expect(result.current.step1Data).toEqual(step1);
  });

  it("chama registerFn e loginFn e navega no submit step 2", async () => {
    const registerFn = vi.fn().mockResolvedValue(undefined);
    const loginFn = vi.fn().mockResolvedValue(undefined);
    const navigate = vi.fn();

    const { result } = renderHook(() =>
      useRegisterForm(registerFn, loginFn, navigate),
    );

    act(() => {
      result.current.handleStep1Submit(step1);
    });

    await act(async () => {
      await result.current.handleStep2Submit(step2);
    });

    expect(registerFn).toHaveBeenCalledWith(
      expect.objectContaining({
        username: "joao123",
        email: "joao@example.com",
        password: "123456",
        nome_cliente: "Fazenda Boa Vista",
        codigo_cliente: "1001",
      }),
    );
    expect(loginFn).toHaveBeenCalledWith({
      username: "joao123",
      password: "123456",
    });
    expect(navigate).toHaveBeenCalledWith("/dashboard");
  });

  it("define apiError quando registerFn falha com erro de campo", async () => {
    const registerFn = vi.fn().mockRejectedValue({
      response: {
        data: { codigo_cliente: ["Já existe um cliente com este código."] },
      },
    });

    const { result } = renderHook(() =>
      useRegisterForm(registerFn, vi.fn(), vi.fn()),
    );

    act(() => {
      result.current.handleStep1Submit(step1);
    });

    await act(async () => {
      await result.current.handleStep2Submit(step2);
    });

    expect(result.current.apiError).toBe(
      "Já existe um cliente com este código.",
    );
  });

  it("define mensagem padrão quando registerFn falha sem dados", async () => {
    const registerFn = vi.fn().mockRejectedValue(new Error("network"));

    const { result } = renderHook(() =>
      useRegisterForm(registerFn, vi.fn(), vi.fn()),
    );

    act(() => {
      result.current.handleStep1Submit(step1);
    });

    await act(async () => {
      await result.current.handleStep2Submit(step2);
    });

    expect(result.current.apiError).toBe(
      "Erro ao criar conta. Tente novamente.",
    );
  });
});

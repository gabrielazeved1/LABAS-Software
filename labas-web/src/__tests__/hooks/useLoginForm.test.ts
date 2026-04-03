import { describe, it, expect, vi } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { useLoginForm } from "../../hooks/useLoginForm";

describe("useLoginForm", () => {
  it("inicia sem erro de API", () => {
    const loginFn = vi.fn();
    const { result } = renderHook(() => useLoginForm(loginFn));
    expect(result.current.apiError).toBeNull();
  });

  it("chama loginFn com os dados corretos ao submeter", async () => {
    const loginFn = vi.fn().mockResolvedValue(undefined);
    const { result } = renderHook(() => useLoginForm(loginFn));

    await act(async () => {
      await result.current.onSubmit({ username: "joao", password: "123456" });
    });

    expect(loginFn).toHaveBeenCalledWith({
      username: "joao",
      password: "123456",
    });
    expect(result.current.apiError).toBeNull();
  });

  it("define apiError quando loginFn lança erro com detail", async () => {
    const loginFn = vi.fn().mockRejectedValue({
      response: { data: { detail: "Credenciais inválidas." } },
    });
    const { result } = renderHook(() => useLoginForm(loginFn));

    await act(async () => {
      await result.current.onSubmit({ username: "joao", password: "errada" });
    });

    expect(result.current.apiError).toBe("Credenciais inválidas.");
  });

  it("define mensagem padrão quando loginFn lança erro sem detail", async () => {
    const loginFn = vi.fn().mockRejectedValue(new Error("network"));
    const { result } = renderHook(() => useLoginForm(loginFn));

    await act(async () => {
      await result.current.onSubmit({ username: "joao", password: "errada" });
    });

    expect(result.current.apiError).toBe("Usuário ou senha inválidos.");
  });
});

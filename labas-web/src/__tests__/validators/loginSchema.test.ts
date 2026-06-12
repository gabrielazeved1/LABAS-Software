import { describe, it, expect } from "vitest";
import { loginSchema } from "../../validators/loginSchema";

describe("loginSchema", () => {
  it("aceita dados válidos", () => {
    const result = loginSchema.safeParse({
      username: "joao",
      password: "123456",
    });
    expect(result.success).toBe(true);
  });

  it("rejeita username vazio", () => {
    const result = loginSchema.safeParse({ username: "", password: "123456" });
    expect(result.success).toBe(false);
    expect(result.error?.issues[0].path[0]).toBe("username");
  });

  it("rejeita username com menos de 3 caracteres", () => {
    const result = loginSchema.safeParse({
      username: "ab",
      password: "123456",
    });
    expect(result.success).toBe(false);
    expect(result.error?.issues[0].path[0]).toBe("username");
  });

  it("rejeita password vazia", () => {
    const result = loginSchema.safeParse({ username: "joao", password: "" });
    expect(result.success).toBe(false);
    expect(result.error?.issues[0].path[0]).toBe("password");
  });

  it("rejeita password com menos de 6 caracteres", () => {
    const result = loginSchema.safeParse({ username: "joao", password: "123" });
    expect(result.success).toBe(false);
    expect(result.error?.issues[0].path[0]).toBe("password");
  });
});

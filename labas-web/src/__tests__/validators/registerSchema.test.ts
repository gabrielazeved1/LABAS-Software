import { describe, it, expect } from "vitest";
import { step1Schema, step2Schema } from "../../validators/registerSchema";

describe("step1Schema", () => {
  const validStep1 = {
    username: "joao123",
    email: "joao@example.com",
    password: "123456",
    password2: "123456",
  };

  it("aceita dados válidos", () => {
    expect(step1Schema.safeParse(validStep1).success).toBe(true);
  });

  it("rejeita username com menos de 3 caracteres", () => {
    const result = step1Schema.safeParse({ ...validStep1, username: "jo" });
    expect(result.success).toBe(false);
    expect(result.error?.issues[0].path[0]).toBe("username");
  });

  it("rejeita e-mail inválido", () => {
    const result = step1Schema.safeParse({
      ...validStep1,
      email: "nao-e-email",
    });
    expect(result.success).toBe(false);
    expect(result.error?.issues[0].path[0]).toBe("email");
  });

  it("rejeita password com menos de 6 caracteres", () => {
    const result = step1Schema.safeParse({
      ...validStep1,
      password: "123",
      password2: "123",
    });
    expect(result.success).toBe(false);
    expect(result.error?.issues[0].path[0]).toBe("password");
  });

  it("rejeita quando senhas não coincidem", () => {
    const result = step1Schema.safeParse({
      ...validStep1,
      password2: "outra_senha",
    });
    expect(result.success).toBe(false);
    expect(result.error?.issues[0].path[0]).toBe("password2");
    expect(result.error?.issues[0].message).toBe("As senhas não coincidem");
  });
});

describe("step2Schema", () => {
  const validStep2 = {
    nome_cliente: "Fazenda Boa Vista",
    codigo_cliente: "1001",
  };

  it("aceita dados válidos sem campos opcionais", () => {
    expect(step2Schema.safeParse(validStep2).success).toBe(true);
  });

  it("aceita dados válidos com campos opcionais", () => {
    const result = step2Schema.safeParse({
      ...validStep2,
      municipio: "Uberlândia",
      area: "150.5",
    });
    expect(result.success).toBe(true);
  });

  it("rejeita nome_cliente vazio", () => {
    const result = step2Schema.safeParse({ ...validStep2, nome_cliente: "ab" });
    expect(result.success).toBe(false);
    expect(result.error?.issues[0].path[0]).toBe("nome_cliente");
  });

  it("rejeita codigo_cliente vazio", () => {
    const result = step2Schema.safeParse({ ...validStep2, codigo_cliente: "" });
    expect(result.success).toBe(false);
    expect(result.error?.issues[0].path[0]).toBe("codigo_cliente");
  });

  it("rejeita codigo_cliente com letras", () => {
    const result = step2Schema.safeParse({
      ...validStep2,
      codigo_cliente: "ABC",
    });
    expect(result.success).toBe(false);
    expect(result.error?.issues[0].path[0]).toBe("codigo_cliente");
  });

  it("rejeita area não numérica", () => {
    const result = step2Schema.safeParse({ ...validStep2, area: "vinte" });
    expect(result.success).toBe(false);
    expect(result.error?.issues[0].path[0]).toBe("area");
  });
});

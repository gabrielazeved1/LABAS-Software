/**
 * Schemas de validação para RegisterPage (step 1 e 2).
 * Princípio S (SRP): arquivo dedicado apenas à validação.
 */
import { z } from "zod";

export const step1Schema = z
  .object({
    username: z.string().min(3, "Mínimo de 3 caracteres"),
    email: z.string().email("E-mail inválido"),
    password: z.string().min(6, "Mínimo de 6 caracteres"),
    password2: z.string().min(1, "Confirme a senha"),
  })
  .refine((d) => d.password === d.password2, {
    message: "As senhas não coincidem",
    path: ["password2"],
  });

export const step2Schema = z.object({
  nome_cliente: z.string().min(3, "Nome é obrigatório"),
  codigo_cliente: z
    .string()
    .min(1, "Código é obrigatório")
    .regex(/^\d+$/, "Apenas números"),
  municipio: z.string().optional(),
  area: z
    .string()
    .optional()
    .refine((v) => !v || !isNaN(Number(v)), {
      message: "Informe um número válido",
    }),
});

export type Step1Data = z.infer<typeof step1Schema>;
export type Step2Data = z.infer<typeof step2Schema>;

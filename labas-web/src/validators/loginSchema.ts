/**
 * Schema de validação para LoginPage.
 * Princípio S (SRP): arquivo dedicado apenas à validação.
 */
import { z } from "zod";

export const loginSchema = z.object({
  username: z
    .string()
    .min(1, "Usuário é obrigatório")
    .min(3, "Mínimo de 3 caracteres"),
  password: z
    .string()
    .min(1, "Senha é obrigatória")
    .min(6, "Mínimo de 6 caracteres"),
});

export type LoginFormData = z.infer<typeof loginSchema>;

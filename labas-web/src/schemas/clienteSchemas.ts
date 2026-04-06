import { z } from "zod";

export const clienteSchema = z.object({
  codigo: z
    .string()
    .min(1, "Código é obrigatório")
    .max(50, "Máximo de 50 caracteres"),
  nome: z
    .string()
    .min(1, "Nome é obrigatório")
    .max(255, "Máximo de 255 caracteres"),
  contato: z.string().max(100, "Máximo de 100 caracteres").optional(),
  municipio: z.string().max(100, "Máximo de 100 caracteres").optional(),
  area: z.string().max(100, "Máximo de 100 caracteres").optional(),
  observacoes: z.string().optional(),
});

export type ClienteSchemaInput = z.input<typeof clienteSchema>;
export type ClienteSchemaOutput = z.output<typeof clienteSchema>;

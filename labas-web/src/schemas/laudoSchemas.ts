import { z } from "zod";

const dateSchema = z.string().regex(/^\d{4}-\d{2}-\d{2}$/, "Data inválida");
const optionalDate = z.union([dateSchema, z.literal("")]);

/** Schema do cabeçalho do Laudo (sem campos de análise). */
export const laudoSchema = z.object({
  cliente_codigo: z.string().min(1, "Cliente é obrigatório"),
  data_emissao: dateSchema,
  data_saida: optionalDate.optional(),
  observacoes: z.string().optional(),
});

export type LaudoFormInput = z.input<typeof laudoSchema>;
export type LaudoForm = z.output<typeof laudoSchema>;

// Reexporta para conveniência de imports já existentes
export { optionalDate, dateSchema };

import { z } from "zod";

const dateSchema = z.string().regex(/^\d{4}-\d{2}-\d{2}$/, "Data inválida");

const nullableNumber = z
  .union([z.coerce.number(), z.literal("")])
  .transform((value) => (value === "" ? null : value));

const optionalDate = z.union([dateSchema, z.literal("")]);

export const laudoSchema = z.object({
  n_lab: z
    .string()
    .min(1, "Nº do laudo é obrigatório")
    .regex(/^\d{4}\/\d{3}$/, "Use o formato AAAA/NNN"),
  cliente_codigo: z.string().min(1, "Cliente é obrigatório"),
  data_entrada: dateSchema,
  data_saida: optionalDate,
  ph_agua: nullableNumber.optional(),
  ph_cacl2: nullableNumber.optional(),
  ph_kcl: nullableNumber.optional(),
  p_m: nullableNumber.optional(),
  p_r: nullableNumber.optional(),
  p_rem: nullableNumber.optional(),
  mo: nullableNumber.optional(),
  s: nullableNumber.optional(),
  b: nullableNumber.optional(),
  k: nullableNumber.optional(),
  na: nullableNumber.optional(),
  ca: nullableNumber.optional(),
  mg: nullableNumber.optional(),
  cu: nullableNumber.optional(),
  fe: nullableNumber.optional(),
  mn: nullableNumber.optional(),
  zn: nullableNumber.optional(),
  al: nullableNumber.optional(),
  h_al: nullableNumber.optional(),
  areia: nullableNumber.optional(),
  argila: nullableNumber.optional(),
  silte: nullableNumber.optional(),
});

export type LaudoFormInput = z.input<typeof laudoSchema>;
export type LaudoForm = z.output<typeof laudoSchema>;
